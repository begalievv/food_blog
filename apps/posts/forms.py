from django import forms

from .models import Post, Comment

# class PostForm(forms.ModelForm):
#
#     class Meta:
#         model = Post
#         fields = ('title', 'author', 'description', 'category')

        # widgets = {
        #     'todo': forms.TextInput(
        #         attrs={
        #             'id': 'inputPassword2',
        #             'class': 'form-control',
        #             'placeholder': 'Add your todo'
        #         }
        #     )
        # }

    # def save(self):
    #     new_todo = Todo.objects.create(
    #         todo= self.cleaned_data["todo"],
    #         author= self.request.User,
    #     )
    #     return new_todo

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('body',)

        widgets = {
            'body': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'write a comment...',
                    'rows': '3',
                }
            )
        }