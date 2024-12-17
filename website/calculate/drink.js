var admin = require("firebase-admin");

var serviceAccount = require("path/to/serviceAccountKey.json");//

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://healthy-food-938d3-default-rtdb.firebaseio.com"
});
//=======================================================
//注意：

//path-to-your-service-account-file.json 是服務帳戶密鑰文件的路徑。
//確保 JSON 文件被安全存放，不要將其提交到版本控制系統（如 GitHub）。
//=======================================================
console.log("Firebase Admin SDK Initialized");

// 創建 Axios 實例
const lineApiClient = axios.create({
    baseURL: 'https://api.line.me/v2/bot/message/push', // LINE Messaging API URL
    headers: {
      Authorization: `Bearer YOUR_ACCESS_TOKEN`, // 替換為您的 LINE Channel Access Token
      'Content-Type': 'application/json'
    },
  });
// module.exports = async function (context, myTimer) {
//     const now = new Date();
//     const currentHour = now.getHours();
//     const currentMinute = now.getMinutes();

//     // 從 Firebase 獲取用戶資料
//     const usersRef = admin.firestore().collection('users');
//     const usersSnapshot = await usersRef.get();

//     if (!usersSnapshot.empty) {
//         usersSnapshot.forEach(doc => {
//             const userData = doc.data();
//             const reminders = userData.reminders;

//             reminders.forEach(reminder => {
//                 const [hour, minute] = reminder.time.split(":").map(Number);

//                 // 如果時間匹配，發送提醒
//                 if (hour === currentHour && minute === currentMinute) {
//                     sendReminder(userData.name, reminder.type);
//                 }
//             });
//         });
//     }
// };

// // 發送提醒 (Line Messaging API 示例)
// async function sendReminder(userName, reminderType) {
//     const lineToken = "YOUR_LINE_MESSAGING_API_ACCESS_TOKEN";
//     let message = `${userName}，別忘了 ${reminderType === 'water_intake' ? '喝水' : '運動'}喔！`;

//     await axios.post(
//         'https://api.line.me/v2/bot/message/push',
//         {
//             to: "USER_LINE_ID",
//             messages: [{ type: 'text', text: message }]
//         },
//         {
//             headers: {
//                 Authorization: `Bearer ${lineToken}`,
//                 'Content-Type': 'application/json'
//             }
//         }
//     );
// }
