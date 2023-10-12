from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        total_post_rating = self.posts.aggregate(models.Sum('rating'))['rating__sum'] or 0
        total_comment_rating = self.user_comments.aggregate(models.Sum('rating'))['rating__sum'] or 0
        self.rating = total_post_rating * 3 + total_comment_rating
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Post(models.Model):
    POST_TYPES = (
        ('article', 'Article'),
        ('news', 'News'),
    )
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    post_type = models.CharField(choices=POST_TYPES, max_length=7)
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def preview(self):
        return self.text[:124] + '...'

    def like(self):
        self.rating += 1
        self.save()
        self.author.update_rating()

    def dislike(self):
        self.rating -= 1
        self.save()
        self.author.update_rating()

    def __str__(self):
        return self.title


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.text


    from django.db import models
    from django.contrib.auth.models import User

    class Author(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        rating = models.IntegerField(default=0)

        def __str__(self):
            return self.user.username

        def update_rating(self):
            posts = Post.objects.filter(author=self.id)
            comments = Comment.objects.filter(user=self.id)
            self.rating = sum([post.rating * 3 for post in posts]) + sum([comment.rating for comment in comments])
            self.save()

    class Category(models.Model):
        name = models.CharField(max_length=50, unique=True)

        def __str__(self):
            return self.name

    class Post(models.Model):
        POST_TYPES = (
            ('article', 'Статья'),
            ('news', 'Новость')
        )

        author = models.ForeignKey(Author, on_delete=models.CASCADE)
        post_type = models.CharField(max_length=7, choices=POST_TYPES, default='article')
        created_at = models.DateTimeField(auto_now_add=True)
        title = models.CharField(max_length=100)
        text = models.TextField()
        rating = models.IntegerField(default=0)

        def __str__(self):
            return self.title

        def like(self):
            self.rating += 1
            self.save()

        def dislike(self):
            self.rating -= 1
            self.save()

        def preview(self):
            return self.text[:124] + '...'

    class PostCategory(models.Model):
        post = models.ForeignKey(Post, on_delete=models.CASCADE)
        category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Comment(models.Model):
        post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        created_at = models.DateTimeField(auto_now_add=True)
        text = models.TextField()
        rating = models.IntegerField(default=0)

        def __str__(self):
            return f'Comment by {self.user.username} on {self.post.title}'

        def like(self):
            self.rating += 1
            self.save()

        def dislike(self):
            self.rating -= 1
            self.save()



    #Код  для выполнения задания:

    from django.contrib.auth.models import User
    from blog.models import Author, Category, Post, PostCategory, Comment

    # Создание пользователей
    user1 = User.objects.create_user('user1')
    user2 = User.objects.create_user('user2')

    # Создание авторов
    author1 = Author.objects.create(user=user1)
    author2 = Author.objects.create(user=user2)

    # Создание категорий
    category1 = Category.objects.create(name='Category 1')
    category2 = Category.objects.create(name='Category 2')
    category3 = Category.objects.create(name='Category 3')
    category4 = Category.objects.create(name='Category 4')

    # Создание постов и новостей
    post1 = Post.objects.create(author=author1, post_type='article', title='Post 1', text='Text for post 1', rating=0)
    post2 = Post.objects.create(author=author2, post_type='article', title='Post 2', text='Text for post 2', rating=0)
    news1 = Post.objects.create(author=author1, post_type='news', title='News 1', text='Text for news 1', rating=0)

    # Привязка категорий к постам и новостям
    post_category1 = PostCategory.objects.create(post=post1, category=category1)
    post_category2 = PostCategory.objects.create(post=post1, category=category2)
    post_category3 = PostCategory.objects.create(post=post2, category=category3)
    post_category4 = PostCategory.objects.create(post=news1, category=category4)

    # Создание комментариев
    comment1 = Comment.objects.create(post=post1, user=user1, text='Comment 1 for post 1', rating=0)
    comment2 = Comment.objects.create(post=post2, user=user2, text='Comment 1 for post 2', rating=0)
    comment3 = Comment.objects.create(post=post2, user=user1, text='Comment 2 for post 2', rating=0)
    comment4 = Comment.objects.create(post=news1, user=user2, text='Comment for news 1', rating=0)

    # Лайки и дислайки
    post1.like()
    post2.dislike()
    comment1.like()
    comment2.dislike()

    # Обновление рейтинга авторов
    author1.update_rating()
    author2.update_rating()

    # Вывод лучшего автора
    best_author = Author.objects.all().order_by('-rating').first()
    print(best_author.user.username, best_author.rating)

    # Вывод лучшей статьи
    best_post = Post.objects.filter(post_type='article').order_by('-rating').first()
    print(best_post.created_at, best_post.author.user.username, best_post.rating, best_post.title, best_post.preview())

    # Вывод всех комментариев к лучшей статье
    for comment in best_post.comments.all():
        print(comment.created_at, comment.user.username, comment.rating, comment.text)
