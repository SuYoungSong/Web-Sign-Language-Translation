from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True,
                             help_text='본인의 이메일을 입력해주세요.')  # required = 빈칸 허용 여부  /  help_text = 필드에 대한 설명
    first_name = forms.CharField(max_length=30, required=True,
                                 help_text='본인의 이름의 성을 입력해주세요.')  # max_length = 최대길이 설정
    last_name = forms.CharField(max_length=30, required=True, help_text='본인의 이름을 입력해주세요.')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email') + UserCreationForm.Meta.fields

    def save(self, commit=True):
        user = super().save(commit=False)  # super -> 부모 클래스 를 가리킨다  그러면 UserCreationForm 에 save 함수를 여기에 사용하는것이다.
        user.email = self.cleaned_data['email']  # cleaned_data = 유효성 검사를 끝마친 데이터들
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class CustomUserUpdateForm(UserChangeForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='변경할 본인의 이름의 성을 입력해주세요.')
    last_name = forms.CharField(max_length=30, required=True, help_text='변경할 본인의 이름을 입력해주세요.')

    password = forms.CharField(
        label="변경할 비밀번호",
        strip=False,
        widget=forms.PasswordInput,
        required=False,
        help_text="비밀번호를 변경하지 않으시려면 비워 두십시오.",
    )
    # 비밀번호 관련 필드 추가
    # new_password1 = forms.CharField(
    #     label="변경할 비밀번호",
    #     widget=forms.PasswordInput, # 비밀번호 변경 전용 Input
    #     required=False,
    #     help_text="비밀번호를 변경하지 않으시려면 비워 두십시오."
    # )
    new_password2 = forms.CharField(
        label="비밀번호 확인",
        widget=forms.PasswordInput,  # 비밀번호 변경 전용 Input
        required=False
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].disabled = True
        self.fields['email'].disabled = True

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
    #         raise forms.ValidationError('이미 사용 중인 이메일 주소입니다.')
    #     return email

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        new_password2 = cleaned_data.get('new_password2')

        # 새로운 비밀번호가 입력되었는지 확인
        if password and not new_password2:
            raise forms.ValidationError("두 번째 비밀번호를 입력하세요.")
        elif username and password and password.startswith(username):
            raise ValueError("사용자 이름과 비밀번호가 유사합니다.")
        elif len(password) < 8:
            raise forms.ValidationError("비밀번호는 8자리 이상이여야 합니다")
        elif password.isdigit():
            raise forms.ValidationError("숫자로만 이루어진 비밀번호는 사용할수 없습니다")
        elif password != new_password2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        # 새로운 비밀번호가 입력되었다면 설정
        new_password = self.cleaned_data.get('password')
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user


class CustomUserDeleteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []

    def __init__(self, *args, **kwargs):
        super(CustomUserDeleteForm, self).__init__(*args, **kwargs)
        self.fields['confirmation'] = forms.BooleanField(
            required=True,
            initial=False,
            widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        )

    def clean_confirmation(self):
        confirmation = self.cleaned_data.get('confirmation')
        if not confirmation:
            raise forms.ValidationError('계정 삭제에 동의해 주세요')
        return confirmation
