# MaximoAnimConverter

To use place all the folder inside your maya version script folder

From the folder place userSetup.py outside the folder directly in the script folder

The folder setup should be
```
<----documents----->
	<-----maya----->
		<-----version#----->
			<-----scripts----->
			userSetup.py
			<-----MaximoAnimConverter----->
```

Open maya and execute the following lines or place them as shelve button

```
converter = mac.Converter()
converter.Construct()
```