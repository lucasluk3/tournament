# Tournament
API that creates a tournament.

## System Requirements

- Python 3.8+

## Dependencies

```http
See requirements.txt
```
## Installation

First clone the project:

```http
git clone https://github.com/lucasluk3/tournament.git
```

Create a virtualenv:

```http
(Windows)
 python3 -m venv env

(Linux)
$ virtualenv env
```

Install the dependencies:

```http
pip install -r requirements.txt
```

Run the project:

```http
uvicorn main:app --reload
```

## API Reference

Iterative Documentation
```http
http://localhost:8000/docs#/
```


#### Create tournament

```http
  POST /tournaments/
```
| Body | Type     | Description                          |
| :-------- | :------- |:-------------------------------------|
| `name`      | `string` | **Required**. Name of the Tournament |

#### List tournaments

```http
  GET /tournaments/
```

| Response | Type      | Description             |
|:---------|:----------|:------------------------|
| `id`     | `integer` | Id of the Tournament.   |
| `name`   | `string`  | Name of the Tournament. |


#### Create competitor

```http
  POST /tournaments/{tournament_id}/competitor/
```
| Body          | Type     | Description                                 |
|:--------------| :------- |:--------------------------------------------|
| `name`        | `string` | **Required**. Name of the Competitor        |
| `description` | `string` | Description of the Competitor |


#### Generate initial matches

```http
  GET /tournaments/{tournament_id}/generate-matches/
```
| Response             | Type     | Description                        |
|:-----------------|:---------|:-----------------------------------|
| `id`             | `int`    | Id of the Competitor |
| `competitor_one` | `object` | Competitor One of the round        |
| `competitor_two` | `object` | Competitor Two of the round        |


#### List tournament matches

```http
  GET /tournaments/{tournament_id}/match/
```
| Response         | Type     | Description                 |
|:-----------------|:---------|:----------------------------|
| `id`             | `int`    | Id of the Competitor        |
| `competitor_one` | `object` | Competitor One of the match |
| `competitor_two` | `object` | Competitor Two of the match |


#### Register match result

```http
  POST /tournaments/{tournament_id}/match/{match_id}/
```
| Body    | Type     | Description                             |
|:------------|:---------|:----------------------------------------|
| `winner_id` | `int`    | Id of the Competitor that win the match |



#### Register match result

```http
  GET /tournaments/{tournament_id}/results/
```
| Body        | Type     | Description                             |
|:------------|:---------|:----------------------------------------|
| `winner_id` | `int`    | Id of the Competitor that win the match |



