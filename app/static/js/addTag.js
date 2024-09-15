var tagCount = 0;

function addTag() {
  var tags = document.getElementById("tags");
  var body = document.getElementById("tag_input");
  var oldVal = body.value;

  tags.innerHTML += `
    <span class="tag is-light is-medium" id="tag-` + tagCount + `" style="margin-bottom: 5px;">
      <p>` + body.value + `</p>
      <button class="delete is-small" onclick="deleteTag(` + tagCount + `); return false;"></button>
    </span>
  `;

  body.value = '';
  tagCount++;

  var tagList = document.getElementById('tagList').value.split(',');
  if (tagList[0] == '') {
    tagList = [];
  }
  tagList.push(oldVal);
  document.getElementById('tagList').value = tagList.join(',');
}

function deleteTag(id) {
  document.getElementById("tag-" + id).outerHTML = "";
}

function clickPress(event) {
  if (event.keyCode == 13) {
    addTag();
  }
}