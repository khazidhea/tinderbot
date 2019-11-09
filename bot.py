from api import tinderAPI
from beauty_predict import beauty_predict


token = "your token"
api = tinderAPI(token)
LIKE_THRESHOLD = 7


persons = api.nearby_persons()
for person in persons:
    print(person)
    person.save()
    image_scores = [beauty_predict(image) for image in person.local_images()]
    print(image_scores)
    image_scores = [score for score in image_scores if score != 0]
    if image_scores:
        avg_score = sum(image_scores) / len(image_scores)
        print(avg_score)
        if avg_score > LIKE_THRESHOLD:
            person.like()
