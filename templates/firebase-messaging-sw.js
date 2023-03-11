importScripts('https://www.gstatic.com/firebasejs/4.8.1/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/4.8.1/firebase-messaging.js');

// Initialize the Firebase app in the service worker by passing in the
// messagingSenderId.
firebase.initializeApp({
  // Replace messagingSenderId with yours
  'messagingSenderId': '363527763746'
});

// Retrieve an instance of Firebase Messaging so that it can handle background
// messages.
const messaging = firebase.messaging();
// [END initialize_firebase_in_sw]

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('./firebase-messaging-sw.js')
        .then((registration) => {
            console.log('Registration is successful, scope is:', registration.scope)
        }).catch((err) => {
            console.log('Service worker Registration failed, error:', err)
        })
}

// If you would like to customize notifications that are received in the
// background (Web app is closed or not in browser focus) then you should
// implement this optional method.
// [START background_handler]
messaging.setBackgroundMessageHandler(function(payload) {
  console.log('[firebase-messaging-sw.js] Received background message ', payload);
  // Customize notification here
  payload = payload.data;
  const notificationTitle = payload.title;
  const notificationOptions = {
    body: payload.body,
    icon: payload.icon_url,
  };

  self.addEventListener('notificationclick', function (event) {
    event.notification.close();
    clients.openWindow(payload.url);
  });

  return self.registration.showNotification(notificationTitle,
      notificationOptions);
});
// [END background_handler]