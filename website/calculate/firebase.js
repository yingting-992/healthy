// Firebase SDK 初始化
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.0.1/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/11.0.1/firebase-analytics.js";
import { getDatabase, ref, set, get, child, update, remove } 
from "https://www.gstatic.com/firebasejs/11.0.1/firebase-database.js";


const firebaseConfig = {
  apiKey: "AIzaSyDzZVKeHHLGIdgrYz7Np3XHEPsk7FbhLIE",
  authDomain: "healthy-food-938d3.firebaseapp.com",
  databaseURL: "https://healthy-food-938d3-default-rtdb.firebaseio.com",
  projectId: "healthy-food-938d3",
  storageBucket: "healthy-food-938d3.appspot.com",
  messagingSenderId: "88881865492",
  appId: "1:88881865492:web:0957c85928202e9c8d9801",
  measurementId: "G-YJ7VXRSBK8"
};

const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const db = getDatabase(app);
let BMI = 0; //BMI計算
let BODYFAT = 0; //體脂率計算
let BMR = 0; //基礎代謝率計算 (BMR)


function checkIDExists(id) {  //檢查某個學號 (id) 是否已存在於 Firebase 中
  const editMode = document.getElementById("editMode");
  //resultDisplay 是 result 元素的 DOM 參考，用於顯示查詢結果的狀態（1、0 或 -99）。
  console.log("checkIDExists:" + id);

  //如果學號存在，則填充表單的相關欄位並顯示計算結果；
  if (!id) {//如果學號不存在，則清空相關欄位並更新結果狀態。
    document.getElementById("editMode").innerText = "";
    document.getElementById("stdnumber").focus();
    return;
  }
  const dbRef = ref(db);
  get(child(dbRef, 'Users/' + id)).then((snapshot) => {
    console.log("Exists:" + snapshot.exists());//如果學號存在 (snapshot.exists() 為 true)：
    //填充 stdnumber、name、gender、age、height 和 weight 的值，並且顯示 Firebase 中儲存的 BMI、BodyFat 和 BMR 計算結果。
    if (snapshot.exists()) {
      // 確保資料欄位存在於 Firebase 中
      document.getElementById("stdnumber").value = snapshot.val().stdnumber || id;
      document.getElementById("name").value = snapshot.val().Name || "";
      document.querySelector(`input[name="gender"][value="${snapshot.val().Gender}"]`).checked = true;
      document.getElementById("age").value = snapshot.val().Age || "";
      document.getElementById("height").value = snapshot.val().Height || "";
      document.getElementById("weight").value = snapshot.val().Weight || "";

      // 計算結果欄位 (選擇時同時顯示計算結果)
      document.getElementById("bmiOutput").innerText = `你的 BMI 是: ${snapshot.val().BMI || "未計算"}`;
      document.getElementById("bodyFatOutput").innerText = `你的體脂率是: ${snapshot.val().BodyFat || "未計算"}%`;
      document.getElementById("bmrOutput").innerText = `你的基礎代謝率是: ${snapshot.val().BMR || "未計算"} 大卡`; 
      calculate()
      //resultDisplay.innerText 被設置為 "1"，表示查詢成功且學號存在。
      //函數返回 "1" 表示找到資料。
      editMode.innerText = "1";
      return "1";
    } else {
      document.getElementById("name").value ="";
      //document.querySelector(`input[name="gender"][value="${snapshot.val().Gender}"]`).checked = true;
      document.getElementById("age").value = "";
      document.getElementById("height").value =  "";
      document.getElementById("weight").value =  "";

      // 計算結果欄位 (選擇時同時顯示計算結果)
      document.getElementById("bmiOutput").innerText = `你的 BMI 是: 未計算`;
      document.getElementById("bodyFatOutput").innerText = `你的體脂率是: 未計算`;
      document.getElementById("bmrOutput").innerText = `你的基礎代謝率是: 未計算`; 
      editMode.innerText = "0"; 
      return "0";
    }
  })
  .catch((error) => {
    console.log("查詢失敗:" + error);
    editMode.innerText = "-99";
    return "-99";
    //console.error("查詢失敗: " + error);
  }) ;
} 
 

//計算數據
function calculate() {
  const gender = document.querySelector('input[name="gender"]:checked').value;
  const age = parseInt(document.getElementById("age").value);
  const height = parseFloat(document.getElementById("height").value);
  const weight = parseFloat(document.getElementById("weight").value);
  // BMI 計算
  const bmi = (weight / ((height / 100) ** 2)).toFixed(2);
  document.getElementById("bmiOutput").innerText = `你的 BMI 是: ${bmi}`;
  let feedbacktext = "";
  if (bmi < 18.5) {
    feedbacktext = ("喔喔~ 你的 BMI 過低");
  } else if (bmi >= 18.5 && bmi < 24) {
    feedbacktext = ("恭喜你! 你的 BMI 正常");
  }
  else if (bmi >= 24 && bmi < 27) {
    feedbacktext = ("哎呀呀 你的 BMI 過重啦!");
  }
  else if (bmi >= 27){
    feedbacktext = ("注意檢康喔! 你的 BMI 肥胖");
  }
  BMI = bmi;
  document.getElementById("bmiFeedback").innerText = feedbacktext;
  // 體脂率計算
  let bodyFat;
  if (gender === "male") {
      bodyFat = (1.20 * bmi + 0.23 * age - 16.2).toFixed(2);
  } else {
      bodyFat = (1.20 * bmi + 0.23 * age - 5.4).toFixed(2);
  }
  BODYFAT = bodyFat;
  document.getElementById("bodyFatOutput").innerText = `你的體脂率是: ${bodyFat}%`;

  // 基礎代謝率計算 (BMR)
  let bmr;
  if (gender === "male") {
      bmr = (88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)).toFixed(2);
  } else {
      bmr = (447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)).toFixed(2);
  }
  BMR = bmr;
  document.getElementById("bmrOutput").innerText = `你的基礎代謝率是: ${bmr} 大卡`;

}
 
function checkID() {
  const stdnumber = document.getElementById("stdnumber").value;
  checkIDExists(stdnumber);
  //alert("checkID:" + stdnumber + "-->" + checkIfExists);
}  

function checkName() {
  const name = document.getElementById("name").value;
  if (!name) {
    document.getElementById("name").focus();
    
    return;
  }
}
// 參考變數
// const bmiForm = document.getElementById("bmiForm");
const insBtn = document.getElementById("Insbtn");
// const selBtn = document.getElementById("Selbtn");
const delBtn = document.getElementById("Delbtn");
let EditStdnumber = document.getElementById("stdnumber");
let EditName = document.getElementById("name");
let calculateActivityBMRBtn= document.getElementById("calculateActivityBMRBtn");

// 事件綁定
insBtn.addEventListener("click", saveAndUpdateData); // 將儲存按鈕設為觸發保存和更新功能
// selBtn.addEventListener("click", selectData);
delBtn.addEventListener("click", deleteData);
calculateActivityBMRBtn.addEventListener("click", calculateActivityBMR);
EditStdnumber.addEventListener("blur", checkID);
EditName.addEventListener("blur", checkName);

function calculateActivityBMR() {
  //活動程度
  var levelValue = document.getElementById("activityLevel").value;//document.querySelector('input[name="activityLevel"]:checked').value;
  //活動模式
  var modeValue=getMode(); 
  //alert("Activity Level:" + levelValue + ",Mode:" + modeValue);
  var TDEE = 0 ;//每日總熱量消耗 (TDEE)
  TDEE = ((BMR * levelValue) + modeValue);                       // Math.round 四捨五入
  let activityBmrOutput = document.getElementById("activityBmrOutput");
  activityBmrOutput.innerText = `你的每日總熱量消耗 (TDEE) 是: ${TDEE} 大卡`;
}
//
//取得活動模式
function getMode() {
  var ele = document.getElementsByName('mode');
  var modeValue = 0;
  var i=0;
  for (i = 0; i < ele.length; i++) {
      if (ele[i].checked)
        modeValue=parseInt(ele[i].value) ;
  }
  return modeValue;
}
// 儲存並更新資料功能
function saveAndUpdateData() {
  const editMode = document.getElementById("editMode").innerText;
  const name = document.getElementById("name").value;
  const stdnumber = document.getElementById("stdnumber").value;
  const gender = document.querySelector('input[name="gender"]:checked').value;
  const age = parseInt(document.getElementById("age").value);
  const height = parseFloat(document.getElementById("height").value);
  const weight = parseFloat(document.getElementById("weight").value);



  /*
  // BMI 計算
  const bmi = (weight / ((height / 100) ** 2)).toFixed(2);
  document.getElementById("bmiOutput").innerText = `你的 BMI 是: ${bmi}`;
  let feedbacktext = "";
  if (bmi < 18.5) {
    feedbacktext = ("喔喔~ 你的 BMI 過低");
  } else if (bmi >= 18.5 && bmi < 24) {
    feedbacktext = ("恭喜你! 你的 BMI 正常");
  }
  else if (bmi >= 24 && bmi < 27) {
    feedbacktext = ("哎呀呀 你的 BMI 過重啦!");
  }
  else if (bmi >= 27){
    feedbacktext = ("注意檢康喔! 你的 BMI 肥胖");
  }
  document.getElementById("bmiFeedback").innerText = feedbacktext;
  // 體脂率計算
  let bodyFat;
  if (gender === "male") {
      bodyFat = (1.20 * bmi + 0.23 * age - 16.2).toFixed(2);
  } else {
      bodyFat = (1.20 * bmi + 0.23 * age - 5.4).toFixed(2);
  }
  document.getElementById("bodyFatOutput").innerText = `你的體脂率是: ${bodyFat}%`;

  // 基礎代謝率計算 (BMR)
  let bmr;
  if (gender === "male") {
      bmr = (88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)).toFixed(2);
  } else {
      bmr = (447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)).toFixed(2);
  }
  document.getElementById("bmrOutput").innerText = `你的基礎代謝率是: ${bmr} 大卡`;
  */
  calculate();// 計算結果欄位 (選擇時同時顯示計算結果)

  if (editMode=='0') {
      set(ref(db, 'Users/' + stdnumber), {
          Name: name,
          stdnumber: stdnumber,
          Gender: gender,
          Age: age,
          Height: height,
          Weight: weight,
          BMI: BMI,
          BodyFat: BODYFAT,
          BMR: BMR
      })
      .then(() => {
          alert("Data Inserted Successfully");
          document.getElementById("editMode").innerText = '1';
      })
      .catch((error) => {
          alert("Data Insertion Failed: " + error);
      });
  }
  else {
    // 將資料保存到 Firebase
    update(ref(db, 'Users/' + stdnumber), {
        Name: name,
        stdnumber: stdnumber,
        Gender: gender,
        Age: age,
        Height: height,
        Weight: weight,
        BMI: BMI,
        BodyFat: BODYFAT,
        BMR: BMR
    })
    .then(() => {
        alert("Data Saved and Updated Successfully");
    })
    .catch((error) => {
        alert("Data Saving and Updating Failed: " + error);
    });
  }

}

// 廢掉選擇資料功能
// // 選擇資料功能
// function selectData() {
//   const stdnumber = document.getElementById("stdnumber").value;
  
//   if (!stdnumber) {
//     alert("Please enter a valid student number.");
//     return;
//   }
  
//   const dbRef = ref(db);
  
//   get(child(dbRef, 'Users/' + stdnumber)).then((snapshot) => {
//     if (snapshot.exists()) {
//       // 確保資料欄位存在於 Firebase 中
//       document.getElementById("name").value = snapshot.val().Name || "";
//       document.getElementById("stdnumber").value = snapshot.val().stdnumber || stdnumber;
//       document.querySelector(`input[name="gender"][value="${snapshot.val().Gender}"]`).checked = true;
//       document.getElementById("age").value = snapshot.val().Age || "";
//       document.getElementById("height").value = snapshot.val().Height || "";
//       document.getElementById("weight").value = snapshot.val().Weight || "";

//       // 計算結果欄位 (選擇時同時顯示計算結果)
//       document.getElementById("bmiOutput").innerText = `你的 BMI 是: ${snapshot.val().BMI || "未計算"}`;
//       document.getElementById("bodyFatOutput").innerText = `你的體脂率是: ${snapshot.val().BodyFat || "未計算"}%`;
//       document.getElementById("bmrOutput").innerText = `你的基礎代謝率是: ${snapshot.val().BMR || "未計算"} 大卡`;
//     } else {
//       alert("No data found");
//     }
//   })
//   .catch((error) => {
//     alert("Data Selection Failed: " + error);
//   });
// }

// 刪除資料功能 (隱藏)
function deleteData(){
  const stdnumber = document.getElementById("stdnumber").value;
  if (!stdnumber) {
      alert("Please enter a valid student number.");
      return;
  }
  remove(ref(db, 'Users/' + stdnumber))
  .then(() => {
      alert("Data Deleted Successfully");
  })
  .catch((error) => {
      alert("Data Deletion Failed: " + error);
  });
}

//回到頂部
document.addEventListener('scroll', function() {
  const floatingTexts = document.querySelectorAll('.floating-text');
  const scrollPosition = window.scrollY;

  floatingTexts.forEach(text => {
      if (scrollPosition > 100) {
          text.style.transform = 'translateY(-10px)';
      } else {
          text.style.transform = 'translateY(0)';
      }
  });
});


function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}


// 計算基礎代謝率
// 當表單提交時執行
function weight() {

}

document.getElementById('calorieForm').addEventListener('submit', function(e) {
  e.preventDefault();// 阻止表單默認提交
  
  // 獲取用戶輸入的卡路里數據
  let weight = parseFloat(document.getElementById('weight').value);

  // 簡單存儲到localStorage (可改為發送至後端API)
  let storedCalories = JSON.parse(localStorage.getItem('calorieData')) || [];
  storedCalories.push({ date: new Date().toLocaleDateString(), weight: weight });
  localStorage.setItem('calorieData', JSON.stringify(storedCalories));
  //document.getElementById('calories').value = null;
  saveAndUpdateData();// 更新資料
  // 更新畫面
  //displayCalories(storedCalories); //2024.12.2 取消 // 更新列表
  //renderCalorieChart(storedCalories); //2024.12.2 取消 // 更新圖表
});

// 當表單Clear時執行
document.getElementById('clearData').addEventListener( 'click',function() {
 
  // 簡單存儲到localStorage (可改為發送至後端API)
  let storedCalories = [];
  localStorage.setItem('calorieData', JSON.stringify(storedCalories));

  // 更新畫面
  //displayCalories(storedCalories); //2024.12.2 取消 
  //renderCalorieChart(storedCalories); //2024.12.2 取消
});



function displayCalories(data) {
  let output = `<h2>卡路里攝取歷史記錄</h2>`;
  output += `<ul>`
  let iCount = data.length;
  let index = 0;
  data.forEach(entry => {
      index++;
      if (index > iCount - 5) {
          output += `<li>${entry.date} - ${entry.weight} kg</li>`;
      }
      //output += `<li>${entry.date} - ${entry.weight} kg</li>`;
  });
  output += `</ul>`;
  
  document.getElementById('calorieOutput').innerHTML = output;
}

// 當頁面加載時或數據更新後渲染圖表
document.addEventListener('DOMContentLoaded', () => { 
  let storedCalories = JSON.parse(localStorage.getItem('calorieData')) || [];
  //renderCalorieChart(storedCalories); //2024.12.2 取消// 正確渲染初始圖表


  const hamburgerMenu = document.getElementById("hamburgerMenu");
  const navbar = document.getElementById("navbar");
 

  // 點擊漢堡菜單後展開導航欄
  hamburgerMenu.addEventListener("click", () => {
      navbar.classList.toggle("show"); // 切换展开效果
  });

  // 点击菜单项后收起导航栏（可选功能）
  navbar.addEventListener("click", (event) => {
      if (event.target.tagName === "A") {
          navbar.classList.remove("show");
      }
  });

});

//#####
let myChart;
function renderCalorieChart(data) {
  let labels = data.map(entry => entry.date);
  let weight = data.map(entry => entry.weight);

  if (myChart) {
      myChart.data.labels = labels;
      myChart.data.datasets[0].data = weight;
      myChart.update(); // 更新圖表而不重新創建
  } 
  // if (myChart) {
  //     myChart.destroy();
  // }
  else {
      const ctx = document.getElementById('calorieChart').getContext('2d');// 獲取畫布
      myChart = new Chart(ctx, {// 創建圖表
          type: 'line',// 折線圖
          data: {
              labels: labels, // x軸
              datasets: [{
                  label: '體重歷史記錄',
                  data: weight, // 體重數據
                  borderColor: 'rgba(75, 192, 192, 1)',
                  borderWidth: 2,
                  fill: false // 不填充
              }]
          },
          options: {// 選項
              maintainAspectRatio: false,// 不保持比例
              responsive: true,// 自適應大小
              scales: {
                  x: {
                      display: true, // 顯示x軸
                      title: {
                          display: true, // 顯示x軸標題
                          text: '日期' // x軸標題
                      }
                  },
                  y: {
                      display: true,
                      title: {
                          display: true,
                          text: '體重'
                      }
                  }
              }
          }
      });
  }
}



