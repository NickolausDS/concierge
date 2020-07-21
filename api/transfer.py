import os
import logging
from django.conf import settings
import globus_sdk

from api.exc import GlobusTransferException

log = logging.getLogger(__name__)


def get_transfer_client(ctoken_obj):
    """
    Get a transfer client from a ConciergeToken (request.auth obj)
    """
    transfer_token = ctoken_obj.get_token(settings.TRANSFER_SCOPE)
    transfer_authorizer = globus_sdk.AccessTokenAuthorizer(transfer_token)
    return globus_sdk.TransferClient(authorizer=transfer_authorizer)


def submit_transfer(auth, source_endpoint, destination_endpoint, data,
                    **kwargs):
    """
    transfer kwargs:
    label="Manifest Service Request xxxx-yy-zzzz",
    verify_checksum=True,
    notify_on_succeeded=False,
    notify_on_failed=False,
    notify_on_inactive=False,
    submission_id=submission_id
    """
    try:
        tc = get_transfer_client(auth)
        tc.endpoint_autoactivate(source_endpoint)
        tc.endpoint_autoactivate(destination_endpoint)
        tdata = globus_sdk.TransferData(tc, source_endpoint,
                                        destination_endpoint, **kwargs)
        for src, dest, is_dir, algorithm, checksum in data:
            if is_dir is True:
                tdata.add_item(src, dest, recursive=True)
            else:
                tdata.add_item(src, dest, external_checksum=checksum,
                               checksum_algorithm=algorithm)
        return tc.submit_transfer(tdata).data
    except globus_sdk.exc.TransferAPIError as tapie:
        # Service Unavailable (503) if Globus Screws up, otherwise assume
        # the user screwed up with a 400
        status_code = 503 if tapie.http_status >= 500 else 400
        if status_code == 503:
            log.critical('Upstream Globus Transfer error!')
            log.exception(tapie)
        raise GlobusTransferException(tapie.message,
                                      status_code=status_code, code=tapie.code)


def transfer_manifest(auth, globus_manifest):
    """
    Submit a validated Globus Manifest. This is intended to be called via
    a serializer after validation has been completed.
    :param auth: request.auth object which should be a ConciergeToken obj
    :param globus_manifest: api.serializers.manifest.ManifestSerializer
    :return:
    """
    manifest_items = globus_manifest['manifest_items']
    source_endpoint = manifest_items[0]['source_ref']['endpoint']
    destination_endpoint = globus_manifest['destination']['endpoint']
    dest_prefix = globus_manifest['destination']['path']
    transfer_data = []
    for item in manifest_items:
        src = item['source_ref']['path']
        dest = os.path.join(dest_prefix, item['dest_path'])
        is_dir = src.endswith('/')
        checksum = item.get('checksum', {})
        alg = checksum.get('algorithm')
        checksum_value = checksum.get('value')
        transfer_data.append((src, dest, is_dir, alg, checksum_value))
    return submit_transfer(auth, source_endpoint,
                           destination_endpoint,
                           transfer_data)