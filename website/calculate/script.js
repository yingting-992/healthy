$(document).ready(function() {
    $(window).scroll(function() {
        if ($(this).scrollTop() > 100) {
            $('#goTop').fadeIn();
        } else {
            $('#goTop').fadeOut();
        }
    });


    $('#goTop').click(function() {
        $('html, body').animate({scrollTop: 0}, 500);
        return false;
    });
});






$(document).ready(function() {
    $('ul li').click(function(event) {

        const offset = $(this).offset();
        const tooltip = $('<div class="tooltip"></div>');
        const title = $(this).data('title');
        const info = $(this).data('info');


        tooltip.html(`<h4>${title}</h4><p>${info}</p>`).appendTo('body');
        tooltip.css({
            top: offset.top + $(this).outerHeight(),
            left: offset.left 
        }).fadeIn(); 


        $(this).one('mouseleave', function() {
            tooltip.fadeOut(function() {
                tooltip.remove(); 
            });
        });


        $(document).on('click.tooltip', function(e) {
            if (!$(e.target).closest('.tooltip').length && !$(e.target).closest('li').length) {
                tooltip.fadeOut(function() {
                    tooltip.remove(); 
                });
                $(document).off('click.tooltip'); 
            }
        });
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const select = document.querySelector(".custom-select");

    select.addEventListener("change", () => {
        select.style.animation = "fadeInOut 0.5s ease-in-out";
        setTimeout(() => {
            select.style.animation = "none";
        }, 500);
    });
});

$(document).ready(function() {
    $(window).scroll(function() {
        if ($(this).scrollTop() > 100) {
            $('#goTop').fadeIn();
        } else {
            $('#goTop').fadeOut();
        }
    });


    $('#goTop').click(function() {
        $('html, body').animate({scrollTop: 0}, 500);
        return false;
    });
});



$(document).ready(function() {
    $('ul li').click(function(event) {

        const offset = $(this).offset();
        const tooltip = $('<div class="tooltip"></div>');
        const title = $(this).data('title');
        const info = $(this).data('info');


        tooltip.html(`<h4>${title}</h4><p>${info}</p>`).appendTo('body');
        tooltip.css({
            top: offset.top + $(this).outerHeight(), 
            left: offset.left 
        }).fadeIn(); 


        $(this).one('mouseleave', function() {
            tooltip.fadeOut(function() {
                tooltip.remove();
            });
        });


        $(document).on('click.tooltip', function(e) {
            if (!$(e.target).closest('.tooltip').length && !$(e.target).closest('li').length) {
                tooltip.fadeOut(function() {
                    tooltip.remove(); 
                });
                $(document).off('click.tooltip');
            }
        });
    });
});


// // 平滑滾動效果
// document.addEventListener("DOMContentLoaded", () => {
//     const saveButton = document.querySelector("#calorieForm button"); // 儲存更改按鈕
//     const calculateButton = document.querySelector("#calculateActivityBMRBtn"); // 計算熱量按鈕
//     const dataOutput = document.querySelector("#dataoutput"); // 計算結果區域
//     const tdeeSection = document.querySelector(".activity-mode-section"); // TDEE 區域

//     // 平滑滾動並添加動畫效果
//     function scrollToElementWithAnimation(element) {
//         // 平滑滾動
//         element.scrollIntoView({
//             behavior: "smooth", // 平滑滾動
//             block: "start", // 將區域頂部對齊
//         });

//         // 添加動畫效果：背景顏色變化
//         setTimeout(() => {
//             element.style.transition = "background-color 0.5s ease";
//             element.style.backgroundColor = "#f0f9f8"; // 高亮顏色
//             setTimeout(() => {
//                 element.style.backgroundColor = "transparent"; // 恢復原色
//             }, 1500); // 1.5秒後恢復
//         }, 500); // 滾動結束後執行
//     }

//     // 點擊儲存更改按鈕後滾動到計算結果
//     saveButton.addEventListener("click", (e) => {
//         e.preventDefault(); // 阻止表單默認提交行為
//         scrollToElementWithAnimation(dataOutput);
//     });

//     // 點擊計算每日所需熱量按鈕後滾動到 TDEE 區域
//     calculateButton.addEventListener("click", () => {
//         scrollToElementWithAnimation(tdeeSection);
//     });
// });


function scrollToElement(element) {
    element.scrollIntoView({
        behavior: "smooth",
        block: "start",
    });

    // 添加短暫動畫效果
    setTimeout(() => {
        element.style.transition = "background-color 0.3s ease";
        element.style.backgroundColor = "#f0f9f8"; // 高亮顏色
        setTimeout(() => {
            element.style.backgroundColor = "transparent"; // 恢復原色
        }, 1000);
    }, 500);
}


/*
document.addEventListener("DOMContentLoaded", () => {
    const hamburgerMenu = document.getElementById("hamburgerMenu");
    const navbar = document.getElementById("navbar");
   

    // 点击汉堡菜单切换显示
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
*/


// // script.js
// document.addEventListener('DOMContentLoaded', function () {
//     fetch('./data.json')
//         .then(response => response.json())
//         .then(data => {
//             const userSelect = document.getElementById('userSelect');
//             const userInfo = document.getElementById('userInfo');

//             // 填充下拉選單
//             data.forEach(user => {
//                 const option = document.createElement('option');
//                 option.value = user.name;
//                 option.textContent = user.name;
//                 userSelect.appendChild(option);
//             });

//             // 顯示選擇的使用者資料
//             userSelect.addEventListener('change', function () {
//                 const selectedUser = data.find(user => user.name === this.value);
//                 if (selectedUser) {
//                     userInfo.innerHTML = `
//                         <p>Name: ${selectedUser.name}</p>
//                         <p>Age: ${selectedUser.age}</p>
//                         <p>Gender: ${selectedUser.gender}</p>
//                         <p>Height: ${selectedUser.height}</p>
//                         <p>Weight: ${selectedUser.weight}</p>
//                     `;
//                     // 計算基礎代謝率
//                     const bmr = calculateBMR(selectedUser);
//                     userInfo.innerHTML += `<p>BMR: ${bmr}</p>`;
//                 } else {
//                     userInfo.innerHTML = '';
//                 }
//             });
//         })
//         .catch(error => console.error('Error:'+error));
// });

// function calculateBMR(user) {
//     if (user.gender === 'Male') {
//         return 88.362 + (13.397 * user.weight) + (4.799 * user.height) - (5.677 * user.age);
//     } else {
//         return 447.593 + (9.247 * user.weight) + (3.098 * user.height) - (4.330 * user.age);
//     }
// }



