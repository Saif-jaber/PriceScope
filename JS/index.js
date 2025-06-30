const searchedInput = document.querySelector("#search-bar")
const searchContainer = document.querySelector("#search-container")
const messageBox = document.querySelector('#message-box')
let isEmpty = 0; // 1 = is not empty , 0 = empty

function goToPageForPrivacypolicy(){
    window.location.href = "TermsAndPolicies.html#privacy-policy"
}

function goToPageForTerms(){
    window.location.href = "TermsAndPolicies.html#terms"
}

function goToPageForCodeOfConduct(){
    window.location.href = "TermsAndPolicies.html#Conduct"
}

searchedInput.addEventListener("input", () => {
    if (searchedInput.value == ""){
        isEmpty = 0;
        searchContainer.style.borderColor = "red";
        messageBox.textContent = "Please enter a product name to start searching"
    }

    else{
        isEmpty = 1;
        searchContainer.style.borderColor = "white"; 
        messageBox.textContent = ""
    }
})

function saveAndSearch(){
    if(isEmpty == 1){
        localStorage.setItem("searchedItem", searchedInput.value.trim())
        window.location.href = "TermsAndPolicies.html"
    }
    else{
        searchContainer.style.borderColor = "red";
        messageBox.textContent = "Please enter a product name to start searching"
    }
}

