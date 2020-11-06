# Airflow Grpc Operator

Fork on Airflow 2.0

Fix Airflow 1.10.x use grpc operator

## Requirements:
```
apache-airflow
grpcio
protobuf
```

## How to use:
```
from airflow_grpc.grpc_operator import GrpcOperator
args = {
    'owner': 'Airflow',
    'start_date': days_ago(1),
}

dag = DAG(
    dag_id='dag_id',
    default_args=args,
    schedule_interval=None
)

def callback(response: Any, **context):
    return response

run_this = GrpcOperator(
    task_id='task_id',
    dag=dag,
    grpc_conn_id='grpc_connection_id_on_admin_connections',
    stub_class=GrpcStubClass,
    call_func='stub_function',
    data={'request': proto_request_data},
    response_callback=callback
)
```
