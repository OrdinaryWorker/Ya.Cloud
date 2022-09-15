# Ya.Cloud
## API Service for storage and downloading files in Net (VPS) like as Ya.Disk, ready for frontend development or mobile application using
### Technologies
* Python 3.7
* Django 2.2
* Django-rest-api

### Launch project in DEV-mode
* Setup and activate venv 'source venv/Scripts/activate'
* Setup plugins from requirements.txt 'pip install -r requirements.txt'
* Appling migrations 'python manage.py migrate'
* Launch Dev-server 'python manage.py runserver'
### Oleg @OrdinaryWorker
### API Documentation on openapi.yaml
### Requests examples:
___
POST http://127.0.0.1:8080/imports
```
#requests body
{
    "items": [
        {
            "type": "FOLDER",
            "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c2269df1"
        }
    ],
    "updateDate": "2022-02-01T12:00:00Z"
}
```
___
RESPONSE
```
[
    {
        "type": "FOLDER",
        "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c2269df1",
        "date": "2022-02-01T12:00:00Z"
    }
]
```
___
GET http://127.0.0.1:8080/nodes/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1
___
```
{
    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
    "url": null,
    "size": 384,
    "date": "2022-02-02T12:00:00Z",
    "type": "FOLDER",
    "parentId": null,
    "children": [
        {
            "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
            "url": null,
            "size": 384,
            "date": "2022-02-02T12:00:00Z",
            "type": "FOLDER",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "children": [
                {
                    "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                    "url": "/file/url1",
                    "size": 128,
                    "date": "2022-02-02T12:00:00Z",
                    "type": "FILE",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "children": null
                },
                {
                    "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                    "url": "/file/url2",
                    "size": 256,
                    "date": "2022-02-02T12:00:00Z",
                    "type": "FILE",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "children": null
                }
            ]
        }
    ]
}
```
___