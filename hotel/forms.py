from django import forms

from .models import RoomInfo, ClientInfo, ReservationInfo, OrderInfo

class ReservationForm(forms.Form):
	roomId = forms.CharField(label='房间号', widget=forms.TextInput(attrs={'class': 'form-control', 'required': True, 'readonly': True}), error_messages={'required': u'必填'})
	name = forms.CharField(label='姓名', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '姓名', 'required': True}), error_messages={'required': u'必填'})
	phone = forms.CharField(label='手机', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '手机号码', 'required': True}), error_messages={'required': u'必填'})
	checkInDate = forms.DateField(label='入住时间', widget=forms.DateInput(attrs={'class': 'form-control', 'data-date-format': "yyyy/mm/dd", 'required': True, 'readonly': True}), error_messages={'required': u'必填'})
	checkOutDate = forms.DateField(label='离开时间', widget=forms.DateInput(attrs={'class': 'form-control', 'data-date-format': "yyyy/mm/dd", 'required': True, 'readonly': True}), error_messages={'required': u'必填'})

	def clean_phone(self):
		phone = self.cleaned_data['phone']
		if len(phone) != 11:
			raise forms.ValidationError(u'请填写正确的手机号码')
		return phone

	def clean_checkOutDate(self):
		checkInDate = self.cleaned_data['checkInDate']
		checkOutDate = self.cleaned_data['checkOutDate']
		if checkOutDate <= checkInDate:
			raise forms.ValidationError(u'请填写正确的离开时间')
		return checkOutDate

class OrderForm(forms.Form):
	roomId = forms.CharField(label='房间号', widget=forms.TextInput(attrs={'class': 'form-control', 'required': True, 'readonly': True}), error_messages={'required': u'必填'})
	name = forms.CharField(label='姓名', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '姓名', 'required': True}), error_messages={'required': u'必填'})
	idNumber = forms.CharField(label='身份证号', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '身份证号', 'required': True}), error_messages={'required': u'必填'})
	phone = forms.CharField(label='手机', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '手机号码', 'required': True}), error_messages={'required': u'必填'})
	checkInDate = forms.DateField(label='入住时间', widget=forms.DateInput(attrs={'class': 'form-control', 'data-date-format': "yyyy/mm/dd", 'required': True, 'readonly': True}), error_messages={'required': u'必填'})
	checkOutDate = forms.DateField(label='离开时间', widget=forms.DateInput(attrs={'class': 'form-control', 'data-date-format': "yyyy/mm/dd", 'required': True, 'readonly': True}), error_messages={'required': u'必填'})

	def clean_idNumber(self):
		idNumber = self.cleaned_data['idNumber']
		if len(idNumber) != 18 and len(idNumber) != 15:
			raise forms.ValidationError(u'请填写正确的身份证号')
		return idNumber

	def clean_phone(self):
		phone = self.cleaned_data['phone']
		if len(phone) != 11:
			raise forms.ValidationError(u'请填写正确的手机号码')
		return phone

	def clean_checkOutDate(self):
		checkInDate = self.cleaned_data['checkInDate']
		checkOutDate = self.cleaned_data['checkOutDate']
		if checkOutDate <= checkInDate:
			raise forms.ValidationError(u'请填写正确的离开时间')
		return checkOutDate

class CheckOutForm(forms.Form):
	roomId = forms.CharField(label='房间号', widget=forms.TextInput(attrs={'class': 'form-control', 'required': True, 'readonly': True}), error_messages={'required': u'必填'})
