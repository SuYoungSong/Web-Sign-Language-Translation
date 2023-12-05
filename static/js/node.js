let idNum = 0;
function addFile(){
    deepCopy();
}

function deepCopy()  {
  // 'test' node 선택
  const fileModule = document.getElementById('file-module-'+idNum);



  // 노드 복사하기 (deep copy)
  const newNode = fileModule.cloneNode(true);

  console.log(newNode)

  // 복사된 Node id 변경하기
  idNum++;
  newNode.id = 'file-module-' + idNum;

  // 복사한 노드 붙여넣기
  fileModule.after(newNode);
}