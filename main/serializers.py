from rest_framework import serializers

from .models import Post, Image, Comment, Like, Rating


class RatingSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Rating
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        rating = Rating.objects.create(author=author, **validated_data)
        return rating


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Like
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        post = validated_data.get('post')
        liked = Like.objects.create(author=author, post=post)
        liked.likes = True if liked.likes is False else False
        liked.save()

        return liked


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    post_title = serializers.SerializerMethodField('get_post_title')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        commented = Comment.objects.create(author=author, **validated_data)
        return commented

    def get_post_title(self, post_comment):
        title = post_comment.post.title
        return title


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    images = ImageSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    rating = RatingSerializer(many=True, required=False)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'text', 'likes', 'rating', 'created_at', 'comments', 'images')

    def create(self, validated_data):
        request = self.context.get('request')
        image_list = request.FILES
        author = request.user
        post = Post.objects.create(author=author, **validated_data)
        for image in image_list.getlist('images'):
            Image.objects.create(post=post, image=image)
        return post

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = ImageSerializer(instance.images, many=True, context=self.context).data
        if representation['likes']:
            representation['likes'] = instance.likes.filter(likes=True).count()
        total_rate = 0
        print(instance.rating.all().count())
        for rate in instance.rating.all():
            total_rate += int(rate.ratings)
            representation['rating'] = total_rate / instance.rating.all().count()
        representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        return representation

