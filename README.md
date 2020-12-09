# Airflow Grpc Operator

Fork on Airflow 2.0

Fix Airflow 1.10.x use grpc operator

## Requirements:
```
apache-airflow
grpcio
protobuf
```

## How to install:
```
pip install airflow-grpc
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

run_this = GrpcOperator(task_id='task_id',
                        dag=dag,
                        grpc_conn_id='your_grpc_connection_id_on_admin_connections',
                        stub_class=YOUR_GRPC_STUB_CLASS,
                        call_func='your_grpc_stub_function',
                        request_data_func=YOUR_GRPC_MESSAGE_FOR_REQUEST,
                        response_callback=YOUR_RESPOSNE_METHOD,
                        xcom_task_id='XCOM_TASK_ID',
                        data=YOUR_REQUEST_DATA_DICT
)

```
