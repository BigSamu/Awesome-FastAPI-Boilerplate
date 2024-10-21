from datetime import datetime

# Intitial Posts
post_data = [
    {
        "id": 1,
        "filename": "sample_data_1.sgy",
        "image_url": "images/sample_data_1.png",
        "provider": "SeisCo 1",
        "location": "North America",
        "reference_number": 123456,
        "created_at": datetime.utcnow()
    },
    {
        "id": 2,
        "filename": "sample_data_2.sgy",
        "image_url": "images/sample_data_2.png",
        "provider": "SeisCo 1",
        "location": "Europe",
        "reference_number":456789,
        "created_at":datetime.utcnow()
    },
    {
        "id": 3,
        "filename": "sample_data_3.sgy",
        "image_url": "images/sample_data_3.png",
        "provider": "SeisCo 2",
        "location": "South Asia",
        "reference_number":456123,
        "created_at":datetime.utcnow()
    },
    {
        "id": 4,
        "filename": "sample_data_4.sgy",
        "image_url": "images/sample_data_4.png",
        "provider": "SeisCo 2",
        "location": "Africa",
        "reference_number":789456,
        "created_at":datetime.utcnow()
    }
]


# Intitial Users
user_data = [
    {
        "id": 1,
        "username": "alice",
        "email": "alice@og1.com",
        "password":"$2b$12$.fT0fTvgeN00DTLF8F2zxefh4kJRqlsaDuW0bDGPBBMidFdg9z5hC",
        "comment_id": 1,
        "created_at":datetime.utcnow()
    },
    {
        "id": 2,
        "username": "bob",
        "email": "bob@og2.com",
        "password":"$2b$12$1WKV9AIlnrPFsfAIaYhBpuju0un/sazY9pH0Xe0R8noGL.btmq8Iu",
        "comment_id": 2,
        "created_at":datetime.utcnow()
    },
    {
        "id": 3,
        "username": "charlie",
        "email": "charlie@og3.com",
        "password":"$2b$12$nzpL8KLon8nZ.RHmLI7vF./kX/LFcFX2utL1a/fzOcFdBaWfqOV2u",
        "comment_id": 3,
        "created_at":datetime.utcnow()
    }
]

# Intitial Companies
comment_data = [
    {
        "id": 1,
        "name": "O&G 1",
        "type": "client",
        "created_at":datetime.utcnow()
    },
    {
        "id": 2,
        "name": "O&G 2",
        "type": "client",
        "created_at":datetime.utcnow()
    },
    {
        "id": 3,
        "name": "O&G 3",
        "type": "client",
        "created_at":datetime.utcnow()
    }
]
