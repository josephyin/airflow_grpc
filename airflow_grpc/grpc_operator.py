from typing import Callable, Optional, List, Dict, Any

from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

from .grpc_hook import GrpcHook


class GrpcOperator(BaseOperator):
    """
    Calls a gRPC endpoint to execute an action
    :param stub_class: The stub client to use for this gRPC call
    :type stub_class: gRPC stub class generated from proto file
    :param call_func: The client function name to call the gRPC endpoint
    :type call_func: gRPC client function name for the endpoint generated from proto file, str
    :param grpc_conn_id: The connection to run the operator against
    :type grpc_conn_id: str
    :param data: The data to pass to the rpc call
    :type data: A dict with key value pairs as kwargs of the call_func
    :param interceptors: A list of gRPC interceptor objects to be used on the channel
    :type interceptors: A list of gRPC interceptor objects, has to be initialized
    :param custom_connection_func: The customized connection function to return channel object
    :type custom_connection_func: A python function that returns channel object, take in
        a connection object, can be a partial function
    :param streaming: A flag to indicate if the call is a streaming call
    :type streaming: boolean
    :param response_callback: The callback function to process the response from gRPC call
    :type response_callback: A python function that process the response from gRPC call,
        takes in response object and context object, context object can be used to perform
        push xcom or other after task actions
    :param log_response: A flag to indicate if we need to log the response
    :type log_response: boolean
    """

    template_fields = ('stub_class', 'call_func', 'data')

    @apply_defaults
    def __init__(
            self,
            stub_class: Callable,
            call_func: str,
            grpc_conn_id: str = "grpc_default",
            data: Optional[dict] = None,
            interceptors: Optional[List[Callable]] = None,
            custom_connection_func: Optional[Callable] = None,
            streaming: bool = False,
            response_callback: Optional[Callable] = None,
            log_response: bool = False,
            *args,
            **kwargs,
    ) -> None:
        super(GrpcOperator, self).__init__(*args, **kwargs)
        self.stub_class = stub_class
        self.call_func = call_func
        self.grpc_conn_id = grpc_conn_id
        self.data = data or {}
        self.interceptors = interceptors
        self.custom_connection_func = custom_connection_func
        self.streaming = streaming
        self.log_response = log_response
        self.response_callback = response_callback

    def _get_grpc_hook(self) -> GrpcHook:
        return GrpcHook(
            self.grpc_conn_id,
            interceptors=self.interceptors,
            custom_connection_func=self.custom_connection_func,
        )

    def execute(self, context) -> None:
        hook = self._get_grpc_hook()
        self.log.info("Calling gRPC service")
        self.log.info("context: {}".format(context))
        # grpc hook always yield
        responses = hook.run(self.stub_class, self.call_func, streaming=self.streaming, data=self.data)

        context.update(self.data)
        self.data = context

        for response in responses:
            self._handle_response(response)

    def _handle_response(self, response: Any) -> None:
        if self.log_response:
            self.log.info(repr(response))
        if self.response_callback:
            self.response_callback(response, **self.data)
