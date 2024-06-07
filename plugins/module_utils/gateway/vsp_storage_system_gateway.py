import json

try:
    from ..common.vsp_constants import Endpoints
    from ..common.ansible_common import dicts_to_dataclass_list
    from ..model.vsp_storage_system_models import *
    from .gateway_manager import VSPConnectionManager
    from ..common.ansible_common import log_entry_exit
except ImportError:
    from common.vsp_constants import Endpoints
    from common.ansible_common import dicts_to_dataclass_list
    from model.vsp_storage_system_models import *
    from .gateway_manager import VSPConnectionManager
    from common.ansible_common import log_entry_exit


class VSPStorageSystemDirectGateway:

    def __init__(self, connection_info):
        self.connectionManager = VSPConnectionManager(
            connection_info.address, connection_info.username, connection_info.password
        )

    @log_entry_exit
    def get_storage_systems(self):
        endPoint = Endpoints.GET_STORAGE_SYSTEMS
        print(endPoint)
        storageSystemsDict = self.connectionManager.get(endPoint)
        return VSPStorageSystemsInfoPfrestList(
            dicts_to_dataclass_list(
                storageSystemsDict["data"], VSPStorageSystemsInfoPfrest
            )
        )

    @log_entry_exit
    def get_storage_system(self, instance):
        # logger = Log()
        path = instance + "?detailInfoType=version"
        endPoint = Endpoints.GET_STORAGE_SYSTEM.format(path)
        print(endPoint)
        storageSystemInfo = self.connectionManager.get(endPoint)
        # print(storageSystemInfo)
        return VSPStorageSystemInfoPfrest(**storageSystemInfo)

    @log_entry_exit
    def get_journal_pools(self, journal_info_query):
        endPoint = Endpoints.GET_JOURNAL_POOLS
        if journal_info_query is not None:
            endPoint += "?journalInfo=" + journal_info_query
        print(endPoint)
        journal_pools = self.connectionManager.get(endPoint)
        if journal_info_query == "detail":
            return VSPDetailedJournalPoolPfrestList(
                dicts_to_dataclass_list(
                    journal_pools["data"], VSPDetailedJournalPoolPfrest
                )
            )
        elif journal_info_query == "basic":
            return VSPBasicJournalPoolPfrestList(
                dicts_to_dataclass_list(
                    journal_pools["data"], VSPBasicJournalPoolPfrest
                )
            )

    @log_entry_exit
    def get_ports(self):
        endPoint = Endpoints.GET_PORTS + "?detailInfoType=portMode"
        print(endPoint)
        ports = self.connectionManager.get(endPoint)
        return VSPPortPfrestList(dicts_to_dataclass_list(ports["data"], VSPPortPfrest))

    @log_entry_exit
    def get_pools(self):
        endPoint = Endpoints.GET_POOLS
        print(endPoint)
        pools = self.connectionManager.get(endPoint)
        return VSPPoolPfrestList(dicts_to_dataclass_list(pools["data"], VSPPoolPfrest))

    @log_entry_exit
    def get_quorum_disks(self):
        endPoint = Endpoints.GET_QUORUM_DISKS
        print(endPoint)
        quorum_disks = self.connectionManager.get(endPoint)
        return VSPQuorumDiskPfrestList(
            dicts_to_dataclass_list(quorum_disks["data"], VSPQuorumDiskPfrest)
        )

    @log_entry_exit
    def get_free_luns(self):
        # endPoint = Endpoints.GET_LDEVS.format("?count=16384&ldevOption=undefined")
        endPoint = Endpoints.GET_LDEVS.format(
            "?count=100&resourceGroupId=0&ldevOption=undefined"
        )
        print(endPoint)
        free_luns = self.connectionManager.get(endPoint)
        return VSPFreeLunPfrestList(
            dicts_to_dataclass_list(free_luns["data"], VSPFreeLunPfrest)
        )

    @log_entry_exit
    def get_syslog_servers(self):
        endPoint = Endpoints.GET_SYSLOG_SERVERS
        print(endPoint)
        syslog_servers = self.connectionManager.get(endPoint)
        return VSPSyslogServerPfrest(**syslog_servers)

    @log_entry_exit
    def get_storage_capacity(self):
        endPoint = Endpoints.GET_STORAGE_CAPACITY
        print(endPoint)
        capacity = self.connectionManager.get(endPoint)
        return VSPStorageCapacitiesPfrest(**capacity)
