from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from database import db
import models, schemas

app = FastAPI(title="Blog API")

@app.on_event("startup")
def startup():
    db.connect()
    db.create_tables([models.Author, models.Post])

@app.on_event("shutdown")
def shutdown():
    if not db.is_closed():
        db.close()

# ---------------- Authors ----------------

@app.post("/authors", response_model=schemas.AuthorOut)
def create_author(author: schemas.AuthorCreate):
    try:
        return models.Author.create(**author.dict())
    except:
        raise HTTPException(400, "Email already exists")

@app.get("/authors", response_model=List[schemas.AuthorOut])
def get_authors():
    return list(models.Author.select())

@app.get("/authors/{id}", response_model=schemas.AuthorOut)
def get_author(id: int):
    try:
        return models.Author.get_by_id(id)
    except models.Author.DoesNotExist:
        raise HTTPException(404, "Author not found")

@app.put("/authors/{id}", response_model=schemas.AuthorOut)
def update_author(id: int, author: schemas.AuthorCreate):
    try:
        a = models.Author.get_by_id(id)
        a.name = author.name
        a.email = author.email
        a.save()
        return a
    except models.Author.DoesNotExist:
        raise HTTPException(404, "Author not found")

@app.delete("/authors/{id}")
def delete_author(id: int):
    try:
        a = models.Author.get_by_id(id)
        a.delete_instance(recursive=True)
        return {"msg": "Author and posts deleted"}
    except models.Author.DoesNotExist:
        raise HTTPException(404, "Author not found")

@app.get("/authors/{id}/posts", response_model=List[schemas.PostOut])
def get_author_posts(id: int):
    try:
        author = models.Author.get_by_id(id)
        query = (models.Post
                 .select(models.Post, models.Author)
                 .join(models.Author)
                 .where(models.Post.author == author))
        return list(query)
    except models.Author.DoesNotExist:
        raise HTTPException(404, "Author not found")

# ---------------- Posts ----------------

@app.post("/posts", response_model=schemas.PostOut)
def create_post(post: schemas.PostCreate):
    try:
        author = models.Author.get_by_id(post.author_id)
    except models.Author.DoesNotExist:
        raise HTTPException(400, "Author does not exist")

    p = models.Post.create(
        title=post.title,
        content=post.content,
        author=author
    )
    return p

@app.get("/posts", response_model=List[schemas.PostOut])
def get_posts(author_id: Optional[int] = Query(None)):
    query = models.Post.select(models.Post, models.Author).join(models.Author)
    if author_id:
        query = query.where(models.Post.author == author_id)
    return list(query)

@app.get("/posts/{id}", response_model=schemas.PostOut)
def get_post(id: int):
    try:
        return (models.Post
                .select(models.Post, models.Author)
                .join(models.Author)
                .where(models.Post.id == id)
                .get())
    except models.Post.DoesNotExist:
        raise HTTPException(404, "Post not found")

@app.put("/posts/{id}", response_model=schemas.PostOut)
def update_post(id: int, post: schemas.PostUpdate):
    try:
        p = models.Post.get_by_id(id)
        if post.title:
            p.title = post.title
        if post.content:
            p.content = post.content
        p.save()
        return p
    except models.Post.DoesNotExist:
        raise HTTPException(404, "Post not found")

@app.delete("/posts/{id}")
def delete_post(id: int):
    try:
        p = models.Post.get_by_id(id)
        p.delete_instance()
        return {"msg": "Post deleted"}
    except models.Post.DoesNotExist:
        raise HTTPException(404, "Post not found")
