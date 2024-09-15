whitelist = sorted([
  "gthompson30",
	"jlei60"
])

courses = sorted([
  'Foundations of Literature',
  'Acting',
  'American Literature',
  'Creative Nonfiction',
  'Asian American Literature',
  'Writing to Make Change',
  'Poetry',
  'Writers Workshop',
  'AP English: American Literary History',
  'AP English: Defining American Voices',
  'AP English: Contemporaries & Classics',
  'AP English: American Places & Perspectives',
  'AP English: Great Books',
  'AP English: Society & Self',
  'Freshman Composition',
  'Existentionalism',
  'Science Fiction',
  'Shakespearean Literature',
  'Writing in the World',
  'Women\'s Voices in Literature',
  'Leadership and Decision Making'
])

teachers = sorted([
  'Maura Dwyer',
  'Eric Ferencz',
  'Katherine Fletcher',
  'Hugh Francis',
  'Kerry Garfinkel',
  'Eric Grossman',
  'Dermot Hannon',
  'Mark Henderson',
  'Minkyu Kim',
  'Katherine Kincaid',
  'David Mandler',
  'Kim Manning',
  'Rosa Mazzurco',
  'Emily Moore',
  'Emilio Nieves',
  'Sophie Oberfield',
  'Alicia Pohan',
  'Julie Sheinman',
  'Ellis Staley',
  'Lauren Stuzin',
  'Annie Thoms',
  'Megan Weller',
  'Alice Yang',
  'Sarah Lifson'
])

templates = {
	'signup': {
		'subject': '[Writing Center] Confirm your email address',
		'plain': '''
			Dear {params[1]},

			Thanks for signing up for a Writing Center {params[2]} account!

			To confirm your sign-up, please click the link below:

			https://127.0.0.1:5000/auth/confirm?email={params[0]}&usertype={params[2]}

			Sincerely,
			Gabriel Thompson, IT Director
		''',
		'html': '''
			<p>Dear <b>{params[1]}</b>,</p>
			<p>Thanks for signing up for a Writing Center {params[2]} account!</p>
			<p>To confirm your registration, please click the button below:</p>
			<p>
				<a href="http://127.0.0.1:5000/auth/confirm?email={params[0]}&usertype={params[2]}">
					<button>Confirm account</button>
				</a>
			</p>
			<p>Sincerely,
			<br>
			Gabriel Thompson, IT Director</p>
		'''
	},
	'completed': {
		'subject': '''[Writing Center] {params[1]} has finished editing your essay!''',
		'plain': '''
			Dear {params[0]},

			Your editor ({params[1]}) has finished editing your essay!

			Please fill click the link below to verify the edits made by the editor, and to complete a feedback form!

			http://127.0.0.1:5000/feedback?id={params[2]}

			Sincerely,
			Gabriel Thompson, IT Director
		''',
		'html': '''
			<p>Dear {params[0]},</p>
			<p>Your editor, <b>{params[1]}</b>, has finished editing your essay!</p>
			<p>Please fill click the button below to verify the edits made by the editor, and to complete a feedback form!</p>
			<p>
				<a href="http://127.0.0.1:5000/feedback?id={params[2]}">
					<button>Give Feedback</button>
				</a>
			</p>
			<p>Sincerely,
			<br>
			Gabriel Thompson, IT Director</p>
		'''
	},
	'matched': {
		'subject': '''[Writing Center] You've been paired''',
		'plain': '''
			Hi yeet chunguser,

			You've been yeet chungused
		''',
		'html': '''
			<p>Hi {params[0]},</p>
			<p>You've been paired with <b>{params[1]}</b>! Their email is {params[2]}@stuy.edu. If your editor does not editor your essay via Google Docs in a timely manner, or does not reach out to you to meet in-person, feel free to contact them or execswritingcenter@gmail.com.</p>
			<br>
			<p>Sincerely,
			<br>
			Gabriel Thompson, IT Director</p>
		'''
	},
	'newrequest': {
		'subject': '''[Writing Center] New Edit Request''',
		'html': '''
			<p>Hi {params[0]},</p>
			<p>A mentee just created a new edit request!</p>
			<p>You can find it on the Writing Center website <a href="http://127.0.0.1:5000/dashboard">here</a></p>
			<br>
			<p>Sincerely,
			<br>
			Gabriel Thompson, IT Director</p>
		''',
		'plain': 'Oh sneaky youre reading the little text next to the subject huh?'
	},
	'editorfeedback': {
		'subject': 'editor feedback for {params[0]}',
		'plain': 'yeet chungus',
		'html': '<p>There was a chungus attack at ground zero for {params[0]}. but in other news, the communicative was {params[1]}, the edits was {params[2]} the overall was {params[3]} the comments was {params[4]}</p>'
	},
	'addhours': {
		'subject': 'Person just added hours',
		'plain': 'yeet',
		'html': '<p>{params[0]} {params[1]} just finished an essay for {params[2]} {params[3]}. They got {params[4]} hours for it.</p>'
	},
	'finish': {
		'subject': '''[Writing Center] Edit receipt for {params[0]} in pd{params[3]} {params[2]}''',
		'plain': '''
			Hi {params[5]},

			This is a feedback form from 
		''',
		'html': '''
			<p>Hi {params[0]},</p>

			<p>Here is the feedback form for {params[1]}'s essay for your {params[2]} class</p>

			<center>
				<table>
					<tr>
						<td style="text-align: right; background-color: rgb(170, 193, 240)">
							<b>Student:</b>
						</td>
						<td style="background-color: rgb(204, 217, 245); width: 35vw;">{params[1]}</td>
					</tr>
					<tr>
						<td style="text-align: right; background-color: rgb(189, 214, 172)">
							<b>Teacher, Class, Period:</b>
						</td>
						<td style="background-color: rgb(220, 233, 213)">{params[0]}, {params[2]}, Period {params[3]}</td>
					</tr>
					<tr>
						<td style="text-align: right; background-color: rgb(170, 193, 240)">
							<b>Editor:</b>
						</td>
						<td style="background-color: rgb(204, 217, 245)">{params[4]}</td>
					</tr>
					<tr>
						<td style="text-align: right; background-color: rgb(189, 214, 172)">
							<b>Date/Time:</b>
						</td>
						<td style="background-color: rgb(220, 233, 213)">{params[5]}</td>
					</tr>
					<tr>
						<td style="text-align: right; background-color: rgb(170, 193, 240)">
							<b>Tags:</b>
						</td>
						<td style="background-color: rgb(204, 217, 245)">{params[6]}</td>
					</tr>
					<tr>
						<td style="text-align: right; background-color: rgb(189, 214, 172)">
							<b>Comments:</b>
						</td>
						<td style="background-color: rgb(220, 233, 213)">{params[7]}</td>
					</tr>
				</table>
			</center>

			<p>-Gabriel Thompson (WC IT Director)</p>
		'''
	},
	'arista': {
		'subject': 'arista hours addition',
		'plain': 'dfsjlldfjshldfkjsjkldfskljdfs',
		'html': '<p>{params[0]} {params[1]} got {params[2]} hours for request with the id {params[3]} and would like to arista {params[4]}</p>'
	},
	'reminder': {
		'subject': 'Hi {params[0]}, there are {params[1]} new Writing Center requests!',
		'plain': 'There are new edit requests on the Writing Center website!',
		'html': '''
			<head>
				<link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
			</head>
			<body>
				<link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
				<p>Hey, <b>{params[0]}</b>! There are {params[1]} new requests for edits on the Writing Center website</p>
				<center><table>{params[2]}</table></center>
			</body>
		'''
	}
}