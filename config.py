import uuid
from datasets import Dataset
import pandas as pd
import os
os.environ["OPENAI_API_KEY"] = "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"

# Evaluation Metrics

import ragas
from ragas.metrics import (
    context_relevancy,
    answer_relevancy,
    faithfulness,
)
from ragas.metrics.critique import harmfulness
from ragas import evaluate


class Config:
  
  def create_contexts(response):
    con = []
    for nodes in response.source_nodes:
      con.append(nodes.text)
    return con
  
  def log_response(query, query_engine):
    response = query_engine.query(query)
    return response
  
  def create_scan_obj(question, answer, context):
    random_uuid = uuid.uuid4()
    random_uuid_str = str(random_uuid)
    scan_id = random_uuid_str
    questions = [question]
    answers = answer
    contexts = [context]

    data_dict = {
    "baseline": Dataset.from_dict({
        "question": questions,
        "contexts": contexts,
        "answer": answers
    })}

    scan_obj = [scan_id,data_dict]
    return scan_obj
  
  def scan(data_dict):
    result = evaluate(
      data_dict["baseline"],
      metrics=[
        context_relevancy,
        faithfulness,
        answer_relevancy,
        harmfulness,
        ],)
    return result
  
  def create_event_log(elist):
    event_list = []
    payload_list = []
    timestamps = []
    for event in elist:
      event_list.append(event.event_type)
      payload_list.append(event.payload)
      timestamps.append(event.time)

    df = pd.DataFrame()
    df['Events'] = event_list
    df['Payloads'] = payload_list
    df['Time'] = timestamps

    return df




