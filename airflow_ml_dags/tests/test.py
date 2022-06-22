import pytest
from airflow.models import DagBag


@pytest.fixture()
def dagbag():
    return DagBag(dag_folder="dags/", include_examples=False)

    
@pytest.mark.parametrize(
    "dag_name, task_num",
    [
        pytest.param("01_dag_get_data", 1)
        pytest.param("02_dag_train_pipeline", 7)
        pytest.param("03_dag_predict", 3)
    ]
)    


def test_dag_loaded(dagbag, dag_name, task_num):
    dag = dagbag.get_dag(dag_id=dag_name)
    assert dagbag.import_errors == {}
    assert dag is not None
    assert len(dag.tasks) == task_num

    
    
def assert_dag_dict_equal(source, dag):
    assert dag.task_dict.keys() == source.keys()
    for task_id, downstream_list in source.items():
        assert dag.has_task(task_id)
        task = dag.get_task(task_id)
        assert task.downstream_task_ids == set(downstream_list)
        

@pytest.mark.parametrize(
    "dag_name, source",
    [
        pytest.param(
            "01_dag_get_data", 
            {"docker-airflow-download": []}
        ),
        pytest.param(
            "02_dag_train_pipeline", 
            {
                "docker-airflow-download": ["docker-airflow-preprocess"],
                "docker-airflow-preprocess": ["wait_for_processed_data", "wait_for_processed_target"],
                "wait_for_processed_data": ["docker-airflow-split"],
                "wait_for_processed_target": ["docker-airflow-split"],
                "docker-airflow-split": ["docker-airflow-train"],
                "docker-airflow-train": ["docker-airflow-validate"],
                "docker-airflow-validate": []
            }
        ),
        pytest.param(
            "03_dag_predict", 
            {
                "docker-airflow-download": ["wait_for_raw_data"],
                "wait_for_raw_data": ["docker-airflow-predict"],
                "docker-airflow-predict": []
            }
        )
    ]
)


        
        
def test_dag_structure(dagbag, dag_name, source):
    dag = dagbag.get_dag(dag_id=dag_name)
    assert_dag_dict_equal(source, dag)