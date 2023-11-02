let activeList = null;

function createItem(name, quantity){
    return {
        'name': name,
        'quantity': quantity
    }
}

function postReq(url, data) {
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
}

/**
 * 
 * 
 **/

var MD5 = function(d){var r = M(V(Y(X(d),8*d.length)));return r.toLowerCase()};function M(d){for(var _,m="0123456789ABCDEF",f="",r=0;r<d.length;r++)_=d.charCodeAt(r),f+=m.charAt(_>>>4&15)+m.charAt(15&_);return f}function X(d){for(var _=Array(d.length>>2),m=0;m<_.length;m++)_[m]=0;for(m=0;m<8*d.length;m+=8)_[m>>5]|=(255&d.charCodeAt(m/8))<<m%32;return _}function V(d){for(var _="",m=0;m<32*d.length;m+=8)_+=String.fromCharCode(d[m>>5]>>>m%32&255);return _}function Y(d,_){d[_>>5]|=128<<_%32,d[14+(_+64>>>9<<4)]=_;for(var m=1732584193,f=-271733879,r=-1732584194,i=271733878,n=0;n<d.length;n+=16){var h=m,t=f,g=r,e=i;f=md5_ii(f=md5_ii(f=md5_ii(f=md5_ii(f=md5_hh(f=md5_hh(f=md5_hh(f=md5_hh(f=md5_gg(f=md5_gg(f=md5_gg(f=md5_gg(f=md5_ff(f=md5_ff(f=md5_ff(f=md5_ff(f,r=md5_ff(r,i=md5_ff(i,m=md5_ff(m,f,r,i,d[n+0],7,-680876936),f,r,d[n+1],12,-389564586),m,f,d[n+2],17,606105819),i,m,d[n+3],22,-1044525330),r=md5_ff(r,i=md5_ff(i,m=md5_ff(m,f,r,i,d[n+4],7,-176418897),f,r,d[n+5],12,1200080426),m,f,d[n+6],17,-1473231341),i,m,d[n+7],22,-45705983),r=md5_ff(r,i=md5_ff(i,m=md5_ff(m,f,r,i,d[n+8],7,1770035416),f,r,d[n+9],12,-1958414417),m,f,d[n+10],17,-42063),i,m,d[n+11],22,-1990404162),r=md5_ff(r,i=md5_ff(i,m=md5_ff(m,f,r,i,d[n+12],7,1804603682),f,r,d[n+13],12,-40341101),m,f,d[n+14],17,-1502002290),i,m,d[n+15],22,1236535329),r=md5_gg(r,i=md5_gg(i,m=md5_gg(m,f,r,i,d[n+1],5,-165796510),f,r,d[n+6],9,-1069501632),m,f,d[n+11],14,643717713),i,m,d[n+0],20,-373897302),r=md5_gg(r,i=md5_gg(i,m=md5_gg(m,f,r,i,d[n+5],5,-701558691),f,r,d[n+10],9,38016083),m,f,d[n+15],14,-660478335),i,m,d[n+4],20,-405537848),r=md5_gg(r,i=md5_gg(i,m=md5_gg(m,f,r,i,d[n+9],5,568446438),f,r,d[n+14],9,-1019803690),m,f,d[n+3],14,-187363961),i,m,d[n+8],20,1163531501),r=md5_gg(r,i=md5_gg(i,m=md5_gg(m,f,r,i,d[n+13],5,-1444681467),f,r,d[n+2],9,-51403784),m,f,d[n+7],14,1735328473),i,m,d[n+12],20,-1926607734),r=md5_hh(r,i=md5_hh(i,m=md5_hh(m,f,r,i,d[n+5],4,-378558),f,r,d[n+8],11,-2022574463),m,f,d[n+11],16,1839030562),i,m,d[n+14],23,-35309556),r=md5_hh(r,i=md5_hh(i,m=md5_hh(m,f,r,i,d[n+1],4,-1530992060),f,r,d[n+4],11,1272893353),m,f,d[n+7],16,-155497632),i,m,d[n+10],23,-1094730640),r=md5_hh(r,i=md5_hh(i,m=md5_hh(m,f,r,i,d[n+13],4,681279174),f,r,d[n+0],11,-358537222),m,f,d[n+3],16,-722521979),i,m,d[n+6],23,76029189),r=md5_hh(r,i=md5_hh(i,m=md5_hh(m,f,r,i,d[n+9],4,-640364487),f,r,d[n+12],11,-421815835),m,f,d[n+15],16,530742520),i,m,d[n+2],23,-995338651),r=md5_ii(r,i=md5_ii(i,m=md5_ii(m,f,r,i,d[n+0],6,-198630844),f,r,d[n+7],10,1126891415),m,f,d[n+14],15,-1416354905),i,m,d[n+5],21,-57434055),r=md5_ii(r,i=md5_ii(i,m=md5_ii(m,f,r,i,d[n+12],6,1700485571),f,r,d[n+3],10,-1894986606),m,f,d[n+10],15,-1051523),i,m,d[n+1],21,-2054922799),r=md5_ii(r,i=md5_ii(i,m=md5_ii(m,f,r,i,d[n+8],6,1873313359),f,r,d[n+15],10,-30611744),m,f,d[n+6],15,-1560198380),i,m,d[n+13],21,1309151649),r=md5_ii(r,i=md5_ii(i,m=md5_ii(m,f,r,i,d[n+4],6,-145523070),f,r,d[n+11],10,-1120210379),m,f,d[n+2],15,718787259),i,m,d[n+9],21,-343485551),m=safe_add(m,h),f=safe_add(f,t),r=safe_add(r,g),i=safe_add(i,e)}return Array(m,f,r,i)}function md5_cmn(d,_,m,f,r,i){return safe_add(bit_rol(safe_add(safe_add(_,d),safe_add(f,i)),r),m)}function md5_ff(d,_,m,f,r,i,n){return md5_cmn(_&m|~_&f,d,_,r,i,n)}function md5_gg(d,_,m,f,r,i,n){return md5_cmn(_&f|m&~f,d,_,r,i,n)}function md5_hh(d,_,m,f,r,i,n){return md5_cmn(_^m^f,d,_,r,i,n)}function md5_ii(d,_,m,f,r,i,n){return md5_cmn(m^(_|~f),d,_,r,i,n)}function safe_add(d,_){var m=(65535&d)+(65535&_);return(d>>16)+(_>>16)+(m>>16)<<16|65535&m}function bit_rol(d,_){return d<<_|d>>>32-_}

async function cloudSync() {
    const response = await fetch(`http://localhost:5000/req/cloudHash/${activeList.getHash()}`)
    let cloudHash = await response.text()
    if(cloudHash === '') return

    let localHash = MD5(`{list_name:${activeList.hash},items:${JSON.stringify(activeList.items)}}`)
    if(localHash == cloudHash)
        console.log('shopping list is syncronized.')
    else
        postReq(
            `http://localhost:5000/req/synchronize/${activeList.getHash()}`,
            activeList.changes
        )
}

setInterval(() => { cloudSync() }, 5000);

/**
 * 
 * CLASS SHOPPING LISTS
 * 
 **/

class ShoppingLists{
    constructor(){
        this.lists = this.load();
        this.render();
    }

    load(){
        const list = localStorage.getItem('shoppingLists');
        return list ? JSON.parse(list) : [];
    }

    save(){
        localStorage.setItem('shoppingLists', JSON.stringify(this.lists));
        this.render()
    }

    create(name){
        const existingList = localStorage.getItem(name)
        if(existingList) return

        this.lists.push(name)
        localStorage.setItem(name, [])

        activeList = new ShoppingList(name)
        this.save()
    }

    delete(item, index){
        this.lists.splice(index, 1);
        localStorage.removeItem(item)

        postReq(
            'http://localhost:5000/req/removeList',
            { list_name: item }
        )
        
        if(activeList.getHash() == item)
            activeList = new ShoppingList(this.getFirst())

        this.save()
    }

    render(){
        const ul = document.getElementById('others');
        ul.innerHTML = '';

        this.lists.forEach((item, index) => {
            const cache = localStorage.getItem(item)
            const list = cache !== '' ? JSON.parse(cache) : []
            const quantity = list.reduce((acc,val) => acc + val.quantity, 0)

            const li = document.createElement('li');
            li.classList = 'px-3 w-100 d-flex justify-content-between align-items-center'
            li.innerHTML = `
                <span>${item}</span>
                <div class="d-flex gap-2 align-items-center">
                    <span class="badge bg-primary rounded-pill">${quantity}</span>
                    <i class="fa-solid fa-delete-left"></i>
                </div>
            `
            li.querySelector('span').addEventListener('click', () => {
                activeList = new ShoppingList(item)
            });

            li.querySelector('i').addEventListener('click', e => {
                e.preventDefault()
                this.delete(item, index);
            });

            ul.appendChild(li);
        });
    }

    getFirst(){
        return this.lists == []
            ? null
            : this.lists[0]
    }
}

const lists = new ShoppingLists()

const addListForm = document.getElementById('addListForm');
addListForm.addEventListener('submit', e => {
    e.preventDefault();

    const input = document.getElementById('list');
    const newList = input.value.trim();
    if(newList !== ''){
        postReq(
            'http://localhost:5000/req/createList', 
            { list_name: newList }
        )

        lists.create(newList)
        input.value = ''
    }
});

/**
 * 
 * CLASS SHOPPING LIST
 * 
 **/

class ShoppingList{
    constructor(hash){
        if(hash == null){
            document.querySelector('h3').innerHTML = `You don't have any lists, please create one.`
        } else{
            this.hash = hash
            this.items = this.load();
            this.changes = this.changelog();
            this.render();
        }
    }

    getHash(){
        return this.hash
    }

    load(){
        const list = localStorage.getItem(this.hash);
        return list ? JSON.parse(list) : [];
    }

    changelog(){
        const cl = localStorage.getItem(`changelog_${this.hash}`)
        return cl ? JSON.parse(cl) : [];
    }

    log(info){
        this.changes.push(info)
        localStorage.setItem(`changelog_${this.hash}`, JSON.stringify(this.changes));
    }

    save() {
        localStorage.setItem(this.hash, JSON.stringify(this.items));
        lists.render()
    }

    modify(func){
        func()
        this.save();
        this.render();
    }

    add(item, quantity) {
        if(this.items.map(i => i.name).includes(item)){
            this.modify(() => { 
                this.items.filter(i => i.name == item)[0].quantity += quantity; 
                this.items = this.items.filter(i => i.quantity > 0)
            })
            this.log({'operation': 'add', 'item': item, 'quantity': quantity})
        }
        else if(quantity > 0){
            this.modify(() => { this.items.push(createItem(item, quantity)); })
            this.log({'operation': 'add', 'item': item, 'quantity': quantity})
        }
    }

    delete(index, quantity) {
        postReq(
            'http://localhost:5000/req/buyItem',
            { list_name: activeList.getHash(), name: this.items[index].name, quantity:quantity}
        )
        
        if(quantity < 1) return
        else if(quantity < this.items[index].quantity)
            this.modify(() => { this.items[index].quantity -= quantity })
        else
            this.modify(() => { this.items.splice(index, 1); })
    }

    rename(item, newName){
        if(newName == '' || item.name == newName) return

        postReq(
            'http://localhost:5000/req/renameItem', 
            { list_name: activeList.getHash(), item_name: item.name, new_item_name: newName }
        )

        if(this.items.map(i => i.name).includes(newName)){
            this.modify(() => { 
                this.items.filter(i => i.name == newName)[0].quantity += item.quantity; 
                this.items = this.items.filter(i => i.name != item.name)
            })
        }
        else
            this.modify(() => { item.name = newName; })
    }

    render() {
        const shoppingList = document.getElementById('shoppingList');
        shoppingList.innerHTML = '';

        document.querySelector('h3').innerHTML = `List: ${this.hash}`

        const deleteModal = document.getElementById('deleteModal')
        const renameModal = document.getElementById('renameModal')

        this.items.forEach((item, index) => {
            const li = document.createElement('li');
            li.classList = 'px-3 w-100 d-flex justify-content-between align-items-center'
            li.innerHTML = `
                <span>${item.name}</span>
                <div class="d-flex gap-2 align-items-center">
                    <span class="badge bg-primary rounded-pill">${item.quantity}</span>
                    <button type="button" class="btn delete" data-bs-toggle="modal" data-bs-target="#deleteModal"><i class="fa-solid fa-cart-shopping"></i></button>
                    <button type="button" class="btn rename" data-bs-toggle="modal" data-bs-target="#renameModal"><i class="fa-solid fa-font"></i></button>
                </div>
            `

            li.querySelector('button.delete').addEventListener('click', () => {
                document.querySelector('#deleteModal #quantity').value = item.quantity
                let action = deleteModal.querySelector('.modal-action')
                action.outerHTML = action.outerHTML; // reset listeners
                action = deleteModal.querySelector('.modal-action')
                action.addEventListener('click', () => {
                    this.delete(index, document.querySelector('#deleteModal #quantity').value);
                })
            })

            li.querySelector('button.rename').addEventListener('click', () => {
                document.getElementById('renameModalLabel').textContent = `Rename item: "${item.name}"`

                let action = renameModal.querySelector('.modal-action')
                action.outerHTML = action.outerHTML; // reset listeners
                action = renameModal.querySelector('.modal-action')
                action.addEventListener('click', () => {
                    this.rename(item, document.getElementById('newName').value)
                })
            })

            shoppingList.appendChild(li);
        });
    }
}

const addItemForm = document.getElementById('addItemForm');
addItemForm.addEventListener('submit', e => {
    e.preventDefault();

    const itemInput = document.getElementById('item');
    const newItem = itemInput.value.trim();

    let quantity = document.getElementById('quantity').value
    if(quantity == '') quantity = 1
    else if(quantity == 0) return
    else quantity = parseInt(quantity)

    if (newItem !== '') {
        postReq(
            'http://localhost:5000/req/addToList', 
            { list_name: activeList.getHash(), item_name: newItem, quantity: quantity }
        )

        activeList.add(newItem, quantity);
        itemInput.value = '';
    }
});


/**
 * 
 * 
 * 
 **/

activeList = new ShoppingList(lists.getFirst())