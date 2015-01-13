// Using $(document).ready never hurts
	$(document).ready(function(){

		// Cookie setting script wrapper
		var cookieScripts = function () {
			// Internal javascript called
			console.log("Running");

			// Loading external javascript file
			$.cookiesDirective.loadScript({
				uri:'external.js',
				appendTo: 'eantics'
			});
		}

		/* Call cookiesDirective, overriding any default params

			*** These are the defaults ***
				explicitConsent: true,
				position: 'top',
				duration: 10,
				limit: 0,
				message: null,
				cookieScripts: null,
				privacyPolicyUri: 'privacy.html',
				scriptWrapper: function(){},
				fontFamily: 'helvetica',
				fontColor: '#FFFFFF',
				fontSize: '13px',
				backgroundColor: '#000000',
				backgroundOpacity: '80',
				linkColor: '#CA0000'

		*/

		$.cookiesDirective({
			privacyPolicyUri: 'myprivacypolicy.html',
			explicitConsent: false,
			position : 'bottom',
			scriptWrapper: cookieScripts,
			cookieScripts: 'Google Analytics, Sumome',
			backgroundColor: '#0cbdaa',
            backgroundOpacity: '99',
			linkColor: '#ffffff'
		});
	});