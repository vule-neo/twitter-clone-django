const commentButton = document.querySelector("#commentButton");
const commentDiv = document.querySelectorAll(".comment-div");

commentButton.addEventListener("click", showCommentSection);

function showCommentSection(){
	if (commentDiv.style.display === "none") {
   		commentDiv.style.display = "block";
  } else {
    	commentDiv.style.display = "none";
  }
}