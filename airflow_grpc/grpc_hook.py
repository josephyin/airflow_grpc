"""GRPC Hook"""
from typing import Callable, Generator, List, Optional

import grpc
from airflow.hooks.base_hook import BaseHook


class GrpcHook(BaseHook):
    """
    General interaction with gRPC servers.
    :param grpc_conn_id: The connection ID to use when fetching connection info.
    :type grpc_conn_id: str
    :param interceptors: a list of gRPC interceptor objects which would be applied
        to the connected gRPC channel. None by default.
    :type interceptors: a list of gRPC interceptors based on or extends the four
        official gRPC interceptors, eg, UnaryUnaryClientInterceptor,
        UnaryStreamClientInterceptor, StreamUnaryClientInterceptor,
        StreamStreamClientInterceptor.
    :param custom_connection_func: The customized connection function to return gRPC channel.
    :type custom_connection_func: python callable objects that accept the connection as
        its only arg. Could be partial or lambda.
    """

    def __init__(
            self,
            grpc_conn_id: str,
            interceptors: Optional[List[Callable]] = None,
            custom_connection_func: Optional[Callable] = None,
    ) -> None:
        super().__init__('grpc')
        self.grpc_conn_id = grpc_conn_id
        self.conn = self.get_connection(self.grpc_conn_id)
        self.extras = self.conn.extra_dejson
        self.interceptors = interceptors if interceptors else []
        self.custom_connection_func = custom_connection_func

    def get_conn(self) -> grpc.Channel:
        base_url = self.conn.host

        if self.conn.port:
            base_url = base_url + ":" + str(self.conn.port)
        channel = grpc.insecure_channel(base_url)
        return channel

    def run(self,
            stub_class: Callable,
            call_func: str,
            streaming: bool = False,
            data: Optional[dict] = None) -> Generator:
        """Call gRPC function and yield response to caller"""
        if data is None:
            data = {}
        with self.get_conn() as channel:
            stub = stub_class(channel)
            try:
                rpc_func = getattr(stub, call_func)
                response = rpc_func(**data)
                if not streaming:
                    yield response
                else:
                    yield from response
            except grpc.RpcError as ex:
                self.log.exception(
                    "Error occurred when calling the grpc service: %s, method: %s \
                    status code: %s, error details: %s",
                    stub.__class__.__name__,
                    call_func,
                    ex.code(),  # pylint: disable=no-member
                    ex.details(),  # pylint: disable=no-member
                )
                raise ex
