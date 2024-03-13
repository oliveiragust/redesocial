function toggleLike(postId) {
    var svg = document.getElementById('my-svg-' + postId);
    var path = svg.getElementsByTagName('path')[0]; // Obtém o primeiro elemento 'path' dentro do SVG

    if (svg.style.fill === 'red' && path.style.stroke === 'red') {
        svg.style.fill = '';
        path.style.stroke = '';
    } else {
        svg.style.fill = 'red';
        path.style.stroke = 'red';
    }
}


document.addEventListener("DOMContentLoaded", function () {
    var postContents = document.querySelectorAll(".post-content");
    postContents.forEach(function (content) {
        var card = content.closest(".card");
        var contentHeight = content.offsetHeight;
        card.style.height = contentHeight + "px";
    });
});




 document.getElementById('post-content').addEventListener('input', function() {
        // Ajuste a altura do campo com base no conteúdo inserido
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });



  function toggleCommentForm(postId) {
        const commentForm = document.getElementById(`comment-form-${postId}`);
        var svg = document.getElementById('my-svg2-' + postId);
        var path = svg.getElementsByTagName('path')[0];


        if (commentForm.style.display === 'none') {
            commentForm.style.display = 'block';
        } else {
            commentForm.style.display = 'none';
        }

         if (svg.style.fill === 'indigo' && path.style.stroke === 'indigo') {
        svg.style.fill = '';
        path.style.stroke = '';
    } else {
        svg.style.fill = 'indigo';
        path.style.stroke = 'indigo';
    }


    }


   function submitComment(postId) {
        var formData = new FormData(document.getElementById("comment-form-" + postId));
        fetch("/comment/" + postId, {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Atualize a seção de comentários apenas para o post correspondente
                document.getElementById("comments-" + postId).innerHTML = data.comments;
            } else {
                alert("Erro ao adicionar comentário. Tente novamente.");
            }
        })
        .catch(error => {
            console.error("Erro ao enviar comentário:", error);
        });
    }


    document.addEventListener("DOMContentLoaded", function() {
    // Adicione um event listener para o envio do formulário
    document.querySelectorAll('form[id^="comment-form-"]').forEach(function(form) {
        form.addEventListener("submit", function(event) {
            // Previne o comportamento padrão de envio do formulário
            event.preventDefault();

            // Obtém o ID do post a partir do ID do formulário
            var postId = this.getAttribute('id').split('-')[2];

            // Chama a função submitComment com o ID do post
            submitComment(postId);
        });
    });
});