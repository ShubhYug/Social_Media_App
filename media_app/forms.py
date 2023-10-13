# myapp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment,Like,Post,Profile


		
class UserForm(UserCreationForm):
	password2 = forms.CharField(label='confirm password (again)',widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('first_name','last_name',"username", "email", "password1", "password2")
		labels = {'email' : 'Email'}

	def save(self, commit=True):
		user = super(UserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        # fields = ['bio','work','education','hobbies','password','link','profile_image','relationship','followers','contact','following','follows']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = '__all__'
        fields = ['content','post_image']

class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = '__all__'


class UserRegisterForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [ 'email', 'password']







# # Create your forms here.
# class Signform(UserCreationForm): 
#     password2 = forms.CharField(label='confirm password (again)',widget=forms.PasswordInput)
#     class Meta:
#         model = User 
#         fields = ['username' 'email'] 
#         labels = {'email' : 'Email'}    

# from django import forms
# from .models import NewUser, Comment, Post, Like

# class UserLoginForm(forms.Form):
#     username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

# class User_Registration_Form(forms.ModelForm):
#     class Meta:
#         model = NewUser
#         fields = '__all__'

# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['text']

# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = '__all__'

# class LikeForm(forms.ModelForm):
#     class Meta:
#         model = Like
#         fields = '__all__'


# class UserRegisterForm(forms.ModelForm):

#     class Meta:
#         model = NewUser
#         fields = [ 'email', 'password']