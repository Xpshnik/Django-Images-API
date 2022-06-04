# Django-Images-API

## Quick setup:

### Build the project:
```bash
docker-compose up --build
```

### Create a superuser:
```bash
docker-compose run app sh -c "python manage.py createsuperuser"
```

Then you can go to http://localhost:8000/admin/ and authenticate.
Inside admin panel you can create a user with account tier assigned:

![image](https://user-images.githubusercontent.com/67806773/171991735-613432ae-ec4c-4375-995c-9e8153b48f8d.png)

and create/modify account tiers:

![image](https://user-images.githubusercontent.com/67806773/171991800-a73558d0-6fc0-4fb5-a5e1-ec3fdab23cfc.png)
**note that expiring links haven't been implemented yet*

Now you're good to make GET requests to http://localhost:8000/api/images if you want to get urls to user's original sized images (depending on user's tier) and thumbnails:

![image](https://user-images.githubusercontent.com/67806773/171992443-7697f8f8-7f77-4157-a67a-eeb8129249b8.png)

To add new images and thumbnails, send POST requests to the same address and get a similar response:

![image](https://user-images.githubusercontent.com/67806773/171992372-f4f24c3d-a7f8-4740-8fb6-c4dfda88d1c7.png)

