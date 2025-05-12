function ShowElement(elemId) {
        let element = document.getElementById(elemId);
        let content = document.querySelectorAll(".content")[0];
        element.style.display='block';
        content.style.background ='rgba(0, 0, 0, 0.8)'
    }

function CloseElement(elemId) {
        let element = document.getElementById(elemId);
        let content = document.querySelectorAll(".content")[0];
        element.style.display='none';
        content.style.background='rgba(0, 0, 0, 0.15)'
    }