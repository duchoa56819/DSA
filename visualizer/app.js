// DSA Visualizer - Core Application
(function(){
const $ = id => document.getElementById(id);
let running = false, stopFlag = false;
const sleep = ms => new Promise(r => {if(stopFlag){throw 'stopped';}setTimeout(r,ms)});

// ---- TABS ----
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(t=>t.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById(btn.dataset.tab+'-tab').classList.add('active');
    if(btn.dataset.tab==='sorting') initSort();
    if(btn.dataset.tab==='searching') initSearch();
    if(btn.dataset.tab==='pathfinding') initPath();
    if(btn.dataset.tab==='ds') initDS();
  });
});

// ============ SORTING ============
let sortArr=[], sortCanvas, sortCtx, comparisons=0, swapCount=0;
function initSort(){
  sortCanvas=$('sort-canvas'); sortCtx=sortCanvas.getContext('2d');
  sortCanvas.width=sortCanvas.parentElement.clientWidth-32;
  sortCanvas.height=350;
  generateArray();
}
function generateArray(){
  const n=parseInt($('sort-size').value);
  sortArr=Array.from({length:n},()=>Math.random()*sortCanvas.height*0.9+10);
  comparisons=0;swapCount=0;
  $('comparisons').textContent='0';$('swaps').textContent='0';$('elapsed').textContent='0ms';
  drawSort([],[]);
}
function drawSort(highlights,sorted){
  const w=sortCanvas.width/sortArr.length;
  sortCtx.fillStyle='#111827';sortCtx.fillRect(0,0,sortCanvas.width,sortCanvas.height);
  sortArr.forEach((v,i)=>{
    if(sorted.includes(i)) sortCtx.fillStyle='#00e676';
    else if(highlights.includes(i)) sortCtx.fillStyle='#7c4dff';
    else sortCtx.fillStyle='#3b82f6';
    sortCtx.fillRect(i*w+1,sortCanvas.height-v,w-2,v);
  });
}
const algInfo={bubble:['Bubble Sort','So sánh từng cặp liền kề, đẩy lớn về cuối. O(n²)'],
selection:['Selection Sort','Tìm min rồi đặt vào đúng vị trí. O(n²)'],
insertion:['Insertion Sort','Chèn phần tử vào vị trí đúng. O(n²)'],
merge:['Merge Sort','Chia đôi, sort, merge. O(n log n)'],
quick:['Quick Sort','Chọn pivot, phân hoạch. O(n log n) avg'],
heap:['Heap Sort','Xây heap rồi extract. O(n log n)']};

$('sort-algo').addEventListener('change',()=>{
  const a=algInfo[$('sort-algo').value];
  $('sort-info').innerHTML=`<h3>${a[0]}</h3><p>${a[1]}</p>`;
});
$('sort-size').addEventListener('input',e=>{$('size-value').textContent=e.target.value;if(!running)generateArray();});
$('sort-speed').addEventListener('input',e=>{$('speed-value').textContent=e.target.value;});
$('sort-reset').addEventListener('click',()=>{if(!running)generateArray();});
$('sort-stop').addEventListener('click',()=>{stopFlag=true;});

$('sort-start').addEventListener('click',async()=>{
  if(running)return;running=true;stopFlag=false;
  comparisons=0;swapCount=0;const t0=performance.now();
  const spd=()=>parseInt($('sort-speed').value);
  const upd=()=>{$('comparisons').textContent=comparisons;$('swaps').textContent=swapCount;
    $('elapsed').textContent=Math.round(performance.now()-t0)+'ms';};
  try{
    const algo=$('sort-algo').value;
    if(algo==='bubble')await bubbleSort(spd,upd);
    else if(algo==='selection')await selectionSort(spd,upd);
    else if(algo==='insertion')await insertionSort(spd,upd);
    else if(algo==='merge')await mergeSortVis(spd,upd);
    else if(algo==='quick')await quickSortVis(0,sortArr.length-1,spd,upd);
    else if(algo==='heap')await heapSortVis(spd,upd);
    drawSort([],sortArr.map((_,i)=>i));
  }catch(e){}
  running=false;upd();
});

async function bubbleSort(spd,upd){
  const n=sortArr.length;
  for(let i=0;i<n;i++){
    for(let j=0;j<n-i-1;j++){
      comparisons++;drawSort([j,j+1],[]);upd();await sleep(spd());
      if(sortArr[j]>sortArr[j+1]){[sortArr[j],sortArr[j+1]]=[sortArr[j+1],sortArr[j]];swapCount++;}
    }
  }
}
async function selectionSort(spd,upd){
  const n=sortArr.length;
  for(let i=0;i<n;i++){
    let mi=i;
    for(let j=i+1;j<n;j++){comparisons++;drawSort([mi,j],[]);upd();await sleep(spd());if(sortArr[j]<sortArr[mi])mi=j;}
    if(mi!==i){[sortArr[i],sortArr[mi]]=[sortArr[mi],sortArr[i]];swapCount++;}
  }
}
async function insertionSort(spd,upd){
  for(let i=1;i<sortArr.length;i++){
    let key=sortArr[i],j=i-1;
    while(j>=0&&sortArr[j]>key){comparisons++;sortArr[j+1]=sortArr[j];j--;swapCount++;drawSort([j+1,i],[]);upd();await sleep(spd());}
    comparisons++;sortArr[j+1]=key;
  }
}
async function mergeSortVis(spd,upd){
  async function ms(l,r){
    if(l>=r)return;const m=Math.floor((l+r)/2);
    await ms(l,m);await ms(m+1,r);
    const tmp=[];let i=l,j=m+1;
    while(i<=m&&j<=r){comparisons++;if(sortArr[i]<=sortArr[j])tmp.push(sortArr[i++]);else tmp.push(sortArr[j++]);}
    while(i<=m)tmp.push(sortArr[i++]);while(j<=r)tmp.push(sortArr[j++]);
    for(let k=0;k<tmp.length;k++){sortArr[l+k]=tmp[k];swapCount++;drawSort([l+k],[]);upd();await sleep(spd());}
  }
  await ms(0,sortArr.length-1);
}
async function quickSortVis(lo,hi,spd,upd){
  if(lo>=hi)return;
  let pivot=sortArr[hi],i=lo-1;
  for(let j=lo;j<hi;j++){comparisons++;drawSort([j,hi],[]);upd();await sleep(spd());
    if(sortArr[j]<=pivot){i++;[sortArr[i],sortArr[j]]=[sortArr[j],sortArr[i]];swapCount++;}
  }
  [sortArr[i+1],sortArr[hi]]=[sortArr[hi],sortArr[i+1]];swapCount++;
  const p=i+1;await quickSortVis(lo,p-1,spd,upd);await quickSortVis(p+1,hi,spd,upd);
}
async function heapSortVis(spd,upd){
  const n=sortArr.length;
  async function siftDown(i,sz){
    let lg=i,l=2*i+1,r=2*i+2;
    if(l<sz){comparisons++;if(sortArr[l]>sortArr[lg])lg=l;}
    if(r<sz){comparisons++;if(sortArr[r]>sortArr[lg])lg=r;}
    if(lg!==i){[sortArr[i],sortArr[lg]]=[sortArr[lg],sortArr[i]];swapCount++;drawSort([i,lg],[]);upd();await sleep(spd());await siftDown(lg,sz);}
  }
  for(let i=Math.floor(n/2)-1;i>=0;i--)await siftDown(i,n);
  for(let i=n-1;i>0;i--){[sortArr[0],sortArr[i]]=[sortArr[i],sortArr[0]];swapCount++;drawSort([0,i],[]);upd();await sleep(spd());await siftDown(0,i);}
}

// ============ SEARCHING ============
let searchArr=[], searchCanvas, searchCtx;
function initSearch(){
  searchCanvas=$('search-canvas');searchCtx=searchCanvas.getContext('2d');
  searchCanvas.width=searchCanvas.parentElement.clientWidth-32;searchCanvas.height=300;
  searchArr=Array.from({length:40},(_,i)=>(i+1)*2);
  drawSearch([],[],-1);
}
function drawSearch(checked,active,found){
  const w=searchCanvas.width/searchArr.length;
  searchCtx.fillStyle='#111827';searchCtx.fillRect(0,0,searchCanvas.width,searchCanvas.height);
  searchArr.forEach((v,i)=>{
    if(i===found)searchCtx.fillStyle='#00e676';
    else if(active.includes(i))searchCtx.fillStyle='#ff9100';
    else if(checked.includes(i))searchCtx.fillStyle='#7c4dff';
    else searchCtx.fillStyle='#3b82f6';
    const h=v/searchArr[searchArr.length-1]*searchCanvas.height*0.85;
    searchCtx.fillRect(i*w+2,searchCanvas.height-h,w-4,h);
    searchCtx.fillStyle='#f0f4f8';searchCtx.font='10px Inter';
    searchCtx.textAlign='center';
    if(searchArr.length<=50)searchCtx.fillText(v,i*w+w/2,searchCanvas.height-h-5);
  });
}
$('search-start').addEventListener('click',async()=>{
  if(running)return;running=true;stopFlag=false;
  const target=parseInt($('search-target').value);
  const algo=$('search-algo').value;let steps=0;
  $('search-result').textContent='Đang tìm...';$('search-steps').textContent='0';
  try{
    if(algo==='linear'){
      for(let i=0;i<searchArr.length;i++){
        steps++;$('search-steps').textContent=steps;
        if(searchArr[i]===target){drawSearch([],[], i);$('search-result').textContent=`Tìm thấy tại index ${i}`;running=false;return;}
        drawSearch(Array.from({length:i+1},(_,j)=>j),[i],-1);await sleep(100);
      }
    }else{
      let lo=0,hi=searchArr.length-1;const checked=[];
      while(lo<=hi){
        const mid=Math.floor((lo+hi)/2);steps++;checked.push(mid);
        $('search-steps').textContent=steps;drawSearch(checked,[mid],-1);await sleep(500);
        if(searchArr[mid]===target){drawSearch(checked,[],mid);$('search-result').textContent=`Tìm thấy tại index ${mid}`;running=false;return;}
        if(searchArr[mid]<target)lo=mid+1;else hi=mid-1;
      }
    }
    $('search-result').textContent='Không tìm thấy';
  }catch(e){}
  running=false;
});
$('search-reset').addEventListener('click',()=>{if(!running)initSearch();});

// ============ PATHFINDING ============
const ROWS=20,COLS=35,EMPTY=0,WALL=1,START=2,END=3,VISITED=4,PATH=5;
let grid=[],startPos=[1,1],endPos=[ROWS-2,COLS-2],pathCanvas,pathCtx,cellSize,mouseDown=false;

function initPath(){
  pathCanvas=$('path-canvas');pathCtx=pathCanvas.getContext('2d');
  pathCanvas.width=pathCanvas.parentElement.clientWidth-32;
  cellSize=Math.floor(pathCanvas.width/COLS);
  pathCanvas.height=ROWS*cellSize;
  grid=Array.from({length:ROWS},()=>Array(COLS).fill(EMPTY));
  grid[startPos[0]][startPos[1]]=START;grid[endPos[0]][endPos[1]]=END;
  drawGrid();
  pathCanvas.onmousedown=e=>{mouseDown=true;toggleWall(e);};
  pathCanvas.onmousemove=e=>{if(mouseDown)toggleWall(e);};
  pathCanvas.onmouseup=()=>mouseDown=false;
  pathCanvas.onmouseleave=()=>mouseDown=false;
}
function toggleWall(e){
  const rect=pathCanvas.getBoundingClientRect();
  const c=Math.floor((e.clientX-rect.left)/cellSize),r=Math.floor((e.clientY-rect.top)/cellSize);
  if(r<0||r>=ROWS||c<0||c>=COLS)return;
  if(grid[r][c]===EMPTY)grid[r][c]=WALL;
  else if(grid[r][c]===WALL)grid[r][c]=EMPTY;
  drawGrid();
}
function drawGrid(){
  const colors={[EMPTY]:'#1a1f2e',[WALL]:'#37474f',[START]:'#00e676',[END]:'#ff1744',[VISITED]:'#7c4dff',[PATH]:'#ffea00'};
  pathCtx.fillStyle='#111827';pathCtx.fillRect(0,0,pathCanvas.width,pathCanvas.height);
  for(let r=0;r<ROWS;r++)for(let c=0;c<COLS;c++){
    pathCtx.fillStyle=colors[grid[r][c]]||'#1a1f2e';
    pathCtx.fillRect(c*cellSize+1,r*cellSize+1,cellSize-2,cellSize-2);
    pathCtx.strokeStyle='#0a0e1a';pathCtx.strokeRect(c*cellSize,r*cellSize,cellSize,cellSize);
  }
}
function generateMaze(){
  grid=Array.from({length:ROWS},()=>Array(COLS).fill(WALL));
  function carve(r,c){
    grid[r][c]=EMPTY;const dirs=[[0,2],[2,0],[0,-2],[-2,0]].sort(()=>Math.random()-0.5);
    for(const[dr,dc]of dirs){const nr=r+dr,nc=c+dc;
      if(nr>0&&nr<ROWS-1&&nc>0&&nc<COLS-1&&grid[nr][nc]===WALL){grid[r+dr/2][c+dc/2]=EMPTY;carve(nr,nc);}
    }
  }
  carve(1,1);grid[startPos[0]][startPos[1]]=START;grid[endPos[0]][endPos[1]]=END;
  // Ensure end is reachable
  grid[endPos[0]-1][endPos[1]]=EMPTY;grid[endPos[0]][endPos[1]-1]=EMPTY;
  drawGrid();
}
$('path-maze').addEventListener('click',()=>{if(!running)generateMaze();});
$('path-reset').addEventListener('click',()=>{if(!running)initPath();});
$('path-start').addEventListener('click',async()=>{
  if(running)return;running=true;stopFlag=false;
  // Clear previous visited/path
  for(let r=0;r<ROWS;r++)for(let c=0;c<COLS;c++)if(grid[r][c]===VISITED||grid[r][c]===PATH)grid[r][c]=EMPTY;
  const algo=$('path-algo').value;
  const prev=Array.from({length:ROWS},()=>Array(COLS).fill(null));
  const dirs=[[0,1],[1,0],[0,-1],[-1,0]];
  let found=false;
  try{
    if(algo==='bfs'||algo==='dijkstra'){
      const q=[[startPos[0],startPos[1]]];const vis=new Set();vis.add(startPos[0]*COLS+startPos[1]);
      while(q.length){
        const[r,c]=q.shift();
        if(r===endPos[0]&&c===endPos[1]){found=true;break;}
        for(const[dr,dc]of dirs){const nr=r+dr,nc=c+dc;const key=nr*COLS+nc;
          if(nr>=0&&nr<ROWS&&nc>=0&&nc<COLS&&!vis.has(key)&&grid[nr][nc]!==WALL){
            vis.add(key);prev[nr][nc]=[r,c];q.push([nr,nc]);
            if(grid[nr][nc]===EMPTY){grid[nr][nc]=VISITED;drawGrid();await sleep(15);}
          }
        }
      }
    }else{
      const vis=new Set();
      async function dfs(r,c){
        if(stopFlag)throw 'stopped';
        if(r===endPos[0]&&c===endPos[1])return true;
        vis.add(r*COLS+c);
        if(grid[r][c]===EMPTY){grid[r][c]=VISITED;drawGrid();await sleep(15);}
        for(const[dr,dc]of dirs){const nr=r+dr,nc=c+dc;
          if(nr>=0&&nr<ROWS&&nc>=0&&nc<COLS&&!vis.has(nr*COLS+nc)&&grid[nr][nc]!==WALL){
            prev[nr][nc]=[r,c];if(await dfs(nr,nc))return true;
          }
        }
        return false;
      }
      found=await dfs(startPos[0],startPos[1]);
    }
    if(found){let[r,c]=endPos;while(prev[r][c]){
      const[pr,pc]=prev[r][c];if(grid[r][c]!==START&&grid[r][c]!==END)grid[r][c]=PATH;
      drawGrid();await sleep(20);r=pr;c=pc;
    }}
  }catch(e){}
  running=false;
});

// ============ DATA STRUCTURES (BST) ============
let bstRoot=null,dsCanvas,dsCtx;
class BSTNode{constructor(v){this.val=v;this.left=null;this.right=null;}}
function bstInsert(node,v){if(!node)return new BSTNode(v);if(v<node.val)node.left=bstInsert(node.left,v);else if(v>node.val)node.right=bstInsert(node.right,v);return node;}
function bstDelete(node,v){if(!node)return null;if(v<node.val)node.left=bstDelete(node.left,v);else if(v>node.val)node.right=bstDelete(node.right,v);
else{if(!node.left)return node.right;if(!node.right)return node.left;let min=node.right;while(min.left)min=min.left;node.val=min.val;node.right=bstDelete(node.right,min.val);}return node;}
let heapArr=[];
function initDS(){dsCanvas=$('ds-canvas');dsCtx=dsCanvas.getContext('2d');dsCanvas.width=dsCanvas.parentElement.clientWidth-32;dsCanvas.height=400;drawDS();}

function drawDS(){
  dsCtx.fillStyle='#111827';dsCtx.fillRect(0,0,dsCanvas.width,dsCanvas.height);
  const type=$('ds-type').value;
  if(type==='bst')drawBST(bstRoot,dsCanvas.width/2,30,dsCanvas.width/4,0);
  else if(type==='heap-vis')drawHeap();
  else drawStack();
}
function drawBST(node,x,y,dx,depth){
  if(!node||depth>8)return;
  if(node.left){dsCtx.strokeStyle='#3b82f6';dsCtx.lineWidth=2;dsCtx.beginPath();dsCtx.moveTo(x,y);dsCtx.lineTo(x-dx,y+55);dsCtx.stroke();drawBST(node.left,x-dx,y+55,dx/2,depth+1);}
  if(node.right){dsCtx.strokeStyle='#3b82f6';dsCtx.lineWidth=2;dsCtx.beginPath();dsCtx.moveTo(x,y);dsCtx.lineTo(x+dx,y+55);dsCtx.stroke();drawBST(node.right,x+dx,y+55,dx/2,depth+1);}
  const grd=dsCtx.createRadialGradient(x,y,0,x,y,20);grd.addColorStop(0,'#7c4dff');grd.addColorStop(1,'#3b82f6');
  dsCtx.fillStyle=grd;dsCtx.beginPath();dsCtx.arc(x,y,18,0,Math.PI*2);dsCtx.fill();
  dsCtx.fillStyle='#fff';dsCtx.font='bold 12px Inter';dsCtx.textAlign='center';dsCtx.textBaseline='middle';dsCtx.fillText(node.val,x,y);
}
function drawHeap(){
  for(let i=0;i<heapArr.length;i++){
    const depth=Math.floor(Math.log2(i+1)),pos=i-Math.pow(2,depth)+1;
    const totalInLevel=Math.pow(2,depth),spacing=dsCanvas.width/(totalInLevel+1);
    const x=spacing*(pos+1),y=40+depth*60;
    const parent=Math.floor((i-1)/2);
    if(i>0){const pd=Math.floor(Math.log2(parent+1)),pp=parent-Math.pow(2,pd)+1;
      const ps=dsCanvas.width/(Math.pow(2,pd)+1),px=ps*(pp+1),py=40+pd*60;
      dsCtx.strokeStyle='#3b82f6';dsCtx.lineWidth=2;dsCtx.beginPath();dsCtx.moveTo(px,py);dsCtx.lineTo(x,y);dsCtx.stroke();}
    dsCtx.fillStyle='#00e676';dsCtx.beginPath();dsCtx.arc(x,y,18,0,Math.PI*2);dsCtx.fill();
    dsCtx.fillStyle='#000';dsCtx.font='bold 12px Inter';dsCtx.textAlign='center';dsCtx.textBaseline='middle';dsCtx.fillText(heapArr[i],x,y);
  }
}
let stackArr=[];
function drawStack(){
  const bw=80,bh=35;const sx=dsCanvas.width/2-bw/2,sy=dsCanvas.height-40;
  dsCtx.strokeStyle='#3b82f6';dsCtx.lineWidth=2;
  dsCtx.strokeRect(sx-5,sy-stackArr.length*bh-10,bw+10,stackArr.length*bh+15);
  stackArr.forEach((v,i)=>{
    const y=sy-i*bh;
    const grd=dsCtx.createLinearGradient(sx,y-bh,sx,y);grd.addColorStop(0,'#7c4dff');grd.addColorStop(1,'#3b82f6');
    dsCtx.fillStyle=grd;dsCtx.fillRect(sx,y-bh+2,bw,bh-4);
    dsCtx.fillStyle='#fff';dsCtx.font='bold 14px Inter';dsCtx.textAlign='center';dsCtx.textBaseline='middle';
    dsCtx.fillText(v,sx+bw/2,y-bh/2+2);
    if(i===stackArr.length-1){dsCtx.fillStyle='#ffea00';dsCtx.font='11px Inter';dsCtx.fillText('← top',sx+bw+30,y-bh/2+2);}
  });
  if(!stackArr.length){dsCtx.fillStyle='#64748b';dsCtx.font='14px Inter';dsCtx.textAlign='center';dsCtx.fillText('Stack rỗng',dsCanvas.width/2,dsCanvas.height/2);}
}

$('ds-insert').addEventListener('click',()=>{
  const v=parseInt($('ds-value').value);if(isNaN(v))return;
  const type=$('ds-type').value;
  if(type==='bst')bstRoot=bstInsert(bstRoot,v);
  else if(type==='heap-vis'){heapArr.push(v);let i=heapArr.length-1;while(i>0){const p=Math.floor((i-1)/2);if(heapArr[p]>heapArr[i]){[heapArr[p],heapArr[i]]=[heapArr[i],heapArr[p]];i=p;}else break;}}
  else stackArr.push(v);
  drawDS();
});
$('ds-delete').addEventListener('click',()=>{
  const v=parseInt($('ds-value').value);const type=$('ds-type').value;
  if(type==='bst')bstRoot=bstDelete(bstRoot,v);
  else if(type==='heap-vis'&&heapArr.length){
    heapArr[0]=heapArr.pop();let i=0;
    while(true){let s=i,l=2*i+1,r=2*i+2;
      if(l<heapArr.length&&heapArr[l]<heapArr[s])s=l;
      if(r<heapArr.length&&heapArr[r]<heapArr[s])s=r;
      if(s===i)break;[heapArr[i],heapArr[s]]=[heapArr[s],heapArr[i]];i=s;}
  }else stackArr.pop();
  drawDS();
});
$('ds-clear').addEventListener('click',()=>{bstRoot=null;heapArr=[];stackArr=[];drawDS();});
$('ds-random').addEventListener('click',()=>{
  const type=$('ds-type').value;
  if(type==='bst'){bstRoot=null;for(let i=0;i<10;i++)bstRoot=bstInsert(bstRoot,Math.floor(Math.random()*99)+1);}
  else if(type==='heap-vis'){heapArr=[];for(let i=0;i<10;i++){heapArr.push(Math.floor(Math.random()*99)+1);let j=heapArr.length-1;while(j>0){const p=Math.floor((j-1)/2);if(heapArr[p]>heapArr[j]){[heapArr[p],heapArr[j]]=[heapArr[j],heapArr[p]];j=p;}else break;}}}
  else{stackArr=[];for(let i=0;i<8;i++)stackArr.push(Math.floor(Math.random()*99)+1);}
  drawDS();
});
$('ds-type').addEventListener('change',drawDS);

// Init
window.addEventListener('load',()=>{initSort();initSearch();initPath();initDS();});
window.addEventListener('resize',()=>{initSort();initSearch();initPath();initDS();});
})();
