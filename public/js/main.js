
function displayFilesToUpload(fileContainer) {
    let fileList = document.getElementById('jd-files-to-upload');
    let html = '<div class="col-md-12">filename</div>'
    let newHTML = '';
    for (let i = 0; i < fileContainer.files['length']; i++) {
        let fileName = fileContainer.files[i]['name'];
        newHTML += html.replace(/filename/g, fileName);
    }

    fileList.innerHTML = newHTML;
}