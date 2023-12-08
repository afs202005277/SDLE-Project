let activeList = null;
let disconnectFromCloud = false;

window.addEventListener("DOMContentLoaded", function () {
    const loader = document.querySelector(".loader");
    const overlay = this.document.querySelector(".overlay");
    setTimeout(() => {
        overlay.style.opacity = 0;
        overlay.style.visibility = 'hidden';
        loader.style.opacity = 0;
        loader.style.visibility = 'hidden';
    }, 500);
    window.addEventListener("beforeunload", function () {
        overlay.style.opacity = 1;
        overlay.style.visibility = 'visible';
        loader.style.opacity = 1;
        loader.style.visibility = 'visible';
    });
},);

document.querySelector('#sideMenuButton').addEventListener('click', function() {
    const menu = document.querySelector('#sideMenu')

    if (menu.style.opacity == 0) {
        menu.style.opacity = 1
        menu.style.width = "320px"
        
    }
    else {
        menu.style.opacity = 0
        menu.style.width = "0px"
    }
})

function loadIcons() {
    const icons = document.querySelectorAll('i')

    for (let i = 0; i < icons.length; i++) {
        if (icons[i].id == 'disconnect-icon') continue;
        icons[i].addEventListener('mouseover', function () {
            icons[i].style.color = "#C63D2F"
        })
        icons[i].addEventListener('mouseleave', function () {
            if (icons[i].classList.contains('whiteIcon')) {
                icons[i].style.color = "#fff"
            }
            else {
                icons[i].style.color = "#000"
            }
            
        })
    }
}

loadIcons()

function createItem(name, quantity) {
    return {
        'name': name,
        'quantity': quantity
    }
}

async function postReq(url, data) {
    if (disconnectFromCloud) throw "Disconnected from cloud";

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });
        return await response.json();
    } catch (error) {
        console.error('Error during POST request:', error);
    }
}

/**
 *
 *
 **/

var MD5 = function (d) {
    var r = M(V(Y(X(d), 8 * d.length)));
    return r.toLowerCase()
};

function M(d) {
    for (var _, m = "0123456789ABCDEF", f = "", r = 0; r < d.length; r++) _ = d.charCodeAt(r), f += m.charAt(_ >>> 4 & 15) + m.charAt(15 & _);
    return f
}

function X(d) {
    for (var _ = Array(d.length >> 2), m = 0; m < _.length; m++) _[m] = 0;
    for (m = 0; m < 8 * d.length; m += 8) _[m >> 5] |= (255 & d.charCodeAt(m / 8)) << m % 32;
    return _
}

function V(d) {
    for (var _ = "", m = 0; m < 32 * d.length; m += 8) _ += String.fromCharCode(d[m >> 5] >>> m % 32 & 255);
    return _
}

function Y(d, _) {
    d[_ >> 5] |= 128 << _ % 32, d[14 + (_ + 64 >>> 9 << 4)] = _;
    for (var m = 1732584193, f = -271733879, r = -1732584194, i = 271733878, n = 0; n < d.length; n += 16) {
        var h = m, t = f, g = r, e = i;
        f = md5_ii(f = md5_ii(f = md5_ii(f = md5_ii(f = md5_hh(f = md5_hh(f = md5_hh(f = md5_hh(f = md5_gg(f = md5_gg(f = md5_gg(f = md5_gg(f = md5_ff(f = md5_ff(f = md5_ff(f = md5_ff(f, r = md5_ff(r, i = md5_ff(i, m = md5_ff(m, f, r, i, d[n + 0], 7, -680876936), f, r, d[n + 1], 12, -389564586), m, f, d[n + 2], 17, 606105819), i, m, d[n + 3], 22, -1044525330), r = md5_ff(r, i = md5_ff(i, m = md5_ff(m, f, r, i, d[n + 4], 7, -176418897), f, r, d[n + 5], 12, 1200080426), m, f, d[n + 6], 17, -1473231341), i, m, d[n + 7], 22, -45705983), r = md5_ff(r, i = md5_ff(i, m = md5_ff(m, f, r, i, d[n + 8], 7, 1770035416), f, r, d[n + 9], 12, -1958414417), m, f, d[n + 10], 17, -42063), i, m, d[n + 11], 22, -1990404162), r = md5_ff(r, i = md5_ff(i, m = md5_ff(m, f, r, i, d[n + 12], 7, 1804603682), f, r, d[n + 13], 12, -40341101), m, f, d[n + 14], 17, -1502002290), i, m, d[n + 15], 22, 1236535329), r = md5_gg(r, i = md5_gg(i, m = md5_gg(m, f, r, i, d[n + 1], 5, -165796510), f, r, d[n + 6], 9, -1069501632), m, f, d[n + 11], 14, 643717713), i, m, d[n + 0], 20, -373897302), r = md5_gg(r, i = md5_gg(i, m = md5_gg(m, f, r, i, d[n + 5], 5, -701558691), f, r, d[n + 10], 9, 38016083), m, f, d[n + 15], 14, -660478335), i, m, d[n + 4], 20, -405537848), r = md5_gg(r, i = md5_gg(i, m = md5_gg(m, f, r, i, d[n + 9], 5, 568446438), f, r, d[n + 14], 9, -1019803690), m, f, d[n + 3], 14, -187363961), i, m, d[n + 8], 20, 1163531501), r = md5_gg(r, i = md5_gg(i, m = md5_gg(m, f, r, i, d[n + 13], 5, -1444681467), f, r, d[n + 2], 9, -51403784), m, f, d[n + 7], 14, 1735328473), i, m, d[n + 12], 20, -1926607734), r = md5_hh(r, i = md5_hh(i, m = md5_hh(m, f, r, i, d[n + 5], 4, -378558), f, r, d[n + 8], 11, -2022574463), m, f, d[n + 11], 16, 1839030562), i, m, d[n + 14], 23, -35309556), r = md5_hh(r, i = md5_hh(i, m = md5_hh(m, f, r, i, d[n + 1], 4, -1530992060), f, r, d[n + 4], 11, 1272893353), m, f, d[n + 7], 16, -155497632), i, m, d[n + 10], 23, -1094730640), r = md5_hh(r, i = md5_hh(i, m = md5_hh(m, f, r, i, d[n + 13], 4, 681279174), f, r, d[n + 0], 11, -358537222), m, f, d[n + 3], 16, -722521979), i, m, d[n + 6], 23, 76029189), r = md5_hh(r, i = md5_hh(i, m = md5_hh(m, f, r, i, d[n + 9], 4, -640364487), f, r, d[n + 12], 11, -421815835), m, f, d[n + 15], 16, 530742520), i, m, d[n + 2], 23, -995338651), r = md5_ii(r, i = md5_ii(i, m = md5_ii(m, f, r, i, d[n + 0], 6, -198630844), f, r, d[n + 7], 10, 1126891415), m, f, d[n + 14], 15, -1416354905), i, m, d[n + 5], 21, -57434055), r = md5_ii(r, i = md5_ii(i, m = md5_ii(m, f, r, i, d[n + 12], 6, 1700485571), f, r, d[n + 3], 10, -1894986606), m, f, d[n + 10], 15, -1051523), i, m, d[n + 1], 21, -2054922799), r = md5_ii(r, i = md5_ii(i, m = md5_ii(m, f, r, i, d[n + 8], 6, 1873313359), f, r, d[n + 15], 10, -30611744), m, f, d[n + 6], 15, -1560198380), i, m, d[n + 13], 21, 1309151649), r = md5_ii(r, i = md5_ii(i, m = md5_ii(m, f, r, i, d[n + 4], 6, -145523070), f, r, d[n + 11], 10, -1120210379), m, f, d[n + 2], 15, 718787259), i, m, d[n + 9], 21, -343485551), m = safe_add(m, h), f = safe_add(f, t), r = safe_add(r, g), i = safe_add(i, e)
    }
    return Array(m, f, r, i)
}

function md5_cmn(d, _, m, f, r, i) {
    return safe_add(bit_rol(safe_add(safe_add(_, d), safe_add(f, i)), r), m)
}

function md5_ff(d, _, m, f, r, i, n) {
    return md5_cmn(_ & m | ~_ & f, d, _, r, i, n)
}

function md5_gg(d, _, m, f, r, i, n) {
    return md5_cmn(_ & f | m & ~f, d, _, r, i, n)
}

function md5_hh(d, _, m, f, r, i, n) {
    return md5_cmn(_ ^ m ^ f, d, _, r, i, n)
}

function md5_ii(d, _, m, f, r, i, n) {
    return md5_cmn(m ^ (_ | ~f), d, _, r, i, n)
}

function safe_add(d, _) {
    var m = (65535 & d) + (65535 & _);
    return (d >> 16) + (_ >> 16) + (m >> 16) << 16 | 65535 & m
}

function bit_rol(d, _) {
    return d << _ | d >>> 32 - _
}

/**
 *
 *
 **/

async function cloudSync() {
    // We arent inside a list
    if (!activeList.getHash()) return

    document.getElementById("sync-overlay").classList.toggle('d-none', false)

    // The list has a ID? (it doesnt has a ID if never got syncronized)
    if (activeList.getId()) {
        let response = await fetch(`http://localhost:6969/req/cloudHash/${activeList.getId()}`)
        let cloudHash = await response.text()
        let localHash = MD5(`{list_name:${activeList.hash},items:${JSON.stringify(activeList.items).replaceAll('\"', '')}}`)

        if (cloudHash == localHash) {
            console.log('shopping list is syncronized.')
            document.getElementById("sync-overlay").classList.toggle('d-none', true)
            return
        }

        console.log('shopping list not syncronized, requesting the cloud.')
        response = await postReq(
            `http://localhost:6969/req/synchronize/${activeList.getId()}`,
            activeList.changes
        )

        console.log(activeList.getId())
        console.log(response)

        localStorage.setItem(activeList.getHash() + "_id", response['id'])
        localStorage.setItem(`changelog_${response['list_name']}`, [])
        localStorage.setItem(activeList.getHash(), JSON.stringify(response['items']));

        document.getElementById('id').textContent = response['id']

        activeList = new ShoppingList(activeList.getHash())
        lists.render()
    } else {
        console.log('shopping list doesnt exists in the cloud, creating...')
        const response = await postReq(
            `http://localhost:6969/req/synchronize/${activeList.getId()}`,
            {
                'name': activeList.getHash(),
                'changes': activeList.changes
            }
        )

        console.log(response);
        localStorage.setItem(response['list_name'] + "_id", response['id'])
        localStorage.setItem(`changelog_${response['list_name']}`, [])

        document.getElementById('id').textContent = response['id']
    }

    document.getElementById("sync-overlay").classList.toggle('d-none', true)
}

function getTimestampInSeconds() {
    // return Math.floor(Date.now() / 1000)
    const date = new Date();
    return Math.floor(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate(), date.getHours(), date.getMinutes(), date.getSeconds()) / 1000);
}

/*
setInterval(() => {
    cloudSync()
}, 5000);
*/

document.getElementById('helper_clear').addEventListener('click', () => {
    localStorage.clear()
    location.reload()
})

document.getElementById('helper_sync').addEventListener('click', cloudSync)

document.getElementById('helper_disc').addEventListener('click', () => {
    if (disconnectFromCloud)
        document.getElementById('helper_disc').textContent = 'Disconnect from cloud'
    else
        document.getElementById('helper_disc').textContent = 'Connect to cloud'

    document.getElementById('disconnect-icon').classList.toggle('d-none', disconnectFromCloud)
    disconnectFromCloud = !disconnectFromCloud
})

/**
 *
 * CLASS SHOPPING LISTS
 *
 **/

class ShoppingLists {
    constructor() {
        this.lists = this.load();
        this.render();
    }

    load() {
        const list = localStorage.getItem('shoppingLists');
        return list ? JSON.parse(list) : [];
    }

    addSharedList(list) {
        const name = list['list_name'];
        const existingList = localStorage.getItem(name)
        if (existingList) return

        this.lists.push(name)
        localStorage.setItem(name, JSON.stringify(list['items']));
        localStorage.setItem(name + "_id", list['id'])
        localStorage.setItem(`changelog_${name}`, [])

        activeList = new ShoppingList(name)
        this.save()
        cloudSync()
    }

    save() {
        localStorage.setItem('shoppingLists', JSON.stringify(this.lists));
        this.render()
    }

    create(name, list_id) {
        const existingList = localStorage.getItem(name)
        if (existingList) return

        this.lists.push(name)
        localStorage.setItem(name, [])
        if (list_id) localStorage.setItem(name + "_id", list_id)

        activeList = new ShoppingList(name)
        this.save()
    }

    delete(item, index) {
        this.lists.splice(index, 1);
        postReq(
            'http://localhost:6969/req/removeList',
            {list_id: localStorage.getItem(`${item}_id`)}
        )
        localStorage.removeItem(item)
        localStorage.removeItem(`changelog_${item}`);
        localStorage.removeItem(`${item}_id`);

        if (activeList.getHash() === item)
            activeList = new ShoppingList(this.getFirst())

        this.save()
    }

    render() {
        const ul = document.getElementById('others');
        ul.innerHTML = '';

        this.lists.forEach((item, index) => {
            const cache = localStorage.getItem(item)
            const list = cache !== '' ? JSON.parse(cache) : []
            const quantity = list.reduce((acc, val) => acc + val.quantity, 0)

            const li = document.createElement('li');
            li.classList = 'px-3 w-100 d-flex justify-content-between align-items-center'
            li.innerHTML = `
                <span>${item}</span>
                <div class="d-flex gap-2 align-items-center">
                    <span class="badge bg-primary rounded-pill">${quantity}</span>
                    <i class="fa-solid fa-delete-left whiteIcon"></i>
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
        loadIcons()
    }

    getFirst() {
        return this.lists == []
            ? null
            : this.lists[0]
    }
}

const lists = new ShoppingLists()

const addListForm = document.getElementById('addListForm');
addListForm.addEventListener('submit', async e => {
    e.preventDefault();

    const input = document.getElementById('list');
    const newList = input.value.trim();

    if (newList !== '') {
        // Do not await for this request, it can block by the ZMQ
        // To be able to use the offline continue execution
        postReq(
            'http://localhost:6969/req/createList',
            {list_name: newList}
        ).then(
            json => {
                console.log(json)
                if (json["status"] === 'existing') {
                    lists.addSharedList(json['data'])
                } else if (json['status'] === 'created') {
                    localStorage.setItem(newList + "_id", json['data']['list_id'])
                    activeList = new ShoppingList(activeList.getHash())
                } else {
                    console.log("Unknown status!")
                }
            }
        )

        // it's not a shared id, not the best solution
        if (newList.length != 32)
            lists.create(newList)

        input.value = ''
    }
});

/**
 *
 * CLASS SHOPPING LIST
 *
 **/

class ShoppingList {
    constructor(hash) {
        if (hash == null) {
            document.querySelector('h3').innerHTML = `You don't have any lists, please create one.`
            document.getElementById('shoppingList').innerHTML = ''
            document.getElementById('id').innerHTML = ''
            if (document.querySelector('#sharing-link-id')) document.querySelector('#sharing-link-id').remove()
            document.querySelector('#formsWrapper').style.display = "none"
        } else {
            this.hash = hash
            this.list_id = localStorage.getItem(hash + "_id")
            this.items = this.load();
            this.changes = this.changelog();
            document.querySelector('#formsWrapper').style.display = "flex"
            this.render();
        }
    }

    clearChangelog() {
        this.changes = [];
    }

    getId() {
        return this.list_id;
    }

    getHash() {
        return this.hash
    }

    load() {
        const list = localStorage.getItem(this.hash);
        return list ? JSON.parse(list) : [];
    }

    changelog() {
        const cl = localStorage.getItem(`changelog_${this.hash}`)
        return cl ? JSON.parse(cl) : [];
    }

    log(info) {
        this.changes.push(info)
        localStorage.setItem(`changelog_${this.hash}`, JSON.stringify(this.changes));
    }

    save() {
        localStorage.setItem(this.hash, JSON.stringify(this.items));
        lists.render()
    }

    modify(func) {
        func()
        this.save();
        this.render();
    }

    add(item, quantity) {
        if (this.items.map(i => i.name).includes(item)) {
            this.modify(() => {
                this.items.filter(i => i.name === item)[0].quantity += quantity;
                this.items = this.items.filter(i => i.quantity >= 0)
            })
            this.log({'operation': 'add', 'item': item, 'quantity': quantity, 'timestamp': getTimestampInSeconds()})
        } else if (quantity > 0) {
            this.modify(() => {
                this.items.push(createItem(item, quantity));
            })
            this.log({'operation': 'add', 'item': item, 'quantity': quantity, 'timestamp': getTimestampInSeconds()})
        }
    }

    delete(index, quantity) {
        const list_name = activeList.getHash()
        postReq(
            'http://localhost:6969/req/buyItem',
            {list_id: activeList.getId(), name: this.items[index].name, quantity: quantity}
        ).then(
            r => {
                if (!r) return

                localStorage.setItem(`changelog_${list_name}`, []);
                if (activeList.getHash() === list_name)
                    activeList.clearChangelog()
            },
            () => {
            }
        )

        if (quantity < 1) return
        else if (quantity < this.items[index].quantity) {
            this.log({
                'operation': 'buy',
                'item': this.items[index].name,
                'quantity': quantity,
                'timestamp': getTimestampInSeconds()
            })
            this.modify(() => {
                this.items[index].quantity -= quantity
            })
        } else {
            this.log({
                'operation': 'buy',
                'item': this.items[index].name,
                'quantity': this.items[index].quantity,
                'timestamp': getTimestampInSeconds()
            })
            this.modify(() => {
                this.items[index].quantity = 0;
            })
        }
    }

    rename(item, newName) {
        if (newName === '' || item.name === newName) return

        const list_name = activeList.getHash()
        postReq(
            'http://localhost:6969/req/renameItem',
            {list_id: activeList.getId(), item_name: item.name, new_item_name: newName}
        ).then(
            r => {
                if (!r) return

                localStorage.setItem(`changelog_${list_name}`, []);
                if (activeList.getHash() === list_name)
                    activeList.clearChangelog()
            },
            () => {
            }
        )

        if (this.items.map(i => i.name).includes(newName)) {
            this.modify(() => {
                this.items.filter(i => i.name === newName)[0].quantity += item.quantity;
                this.items = this.items.filter(i => i.name !== item.name)
            })
            this.log({'operation': 'remove', 'item': item.name, 'timestamp': getTimestampInSeconds()})
            this.log({
                'operation': 'add',
                'item': newName,
                'quantity': item.quantity,
                'timestamp': getTimestampInSeconds()
            })
        } else {
            this.log({
                'operation': 'rename',
                'item': item.name,
                'newItem': newName,
                'timestamp': getTimestampInSeconds()
            })
            this.modify(() => {
                item.name = newName;
            })
        }
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
            li.style.height = "40px";
            if (item.quantity == 0) {
                li.innerHTML = `
                <span style="text-decoration: line-through;">${item.name}</span>
                <div class="d-flex gap-2 align-items-center">
                    <span class="badge bg-primary rounded-pill">${item.quantity}</span>
                </div>
            `
            }
            else {
                li.innerHTML = `
                <span>${item.name}</span>
                <div class="d-flex gap-2 align-items-center">
                    <span class="badge bg-primary rounded-pill">${item.quantity}</span>
                    <button type="button" class="btn delete" data-bs-toggle="modal" data-bs-target="#deleteModal"><i class="fa-solid fa-cart-shopping blackIcon"></i></button>
                    <button type="button" class="btn rename" data-bs-toggle="modal" data-bs-target="#renameModal"><i class="fa-solid fa-font blackIcon"></i></button>
                </div>
            `
            li.querySelector('button.delete').addEventListener('click', () => {
                document.querySelector('#deleteModal #quantity').value = item.quantity
                let action = deleteModal.querySelector('.modal-action')
                action.outerHTML = action.outerHTML; // reset listeners
                action = deleteModal.querySelector('.modal-action')
                action.addEventListener('click', () => {
                    this.delete(index, document.querySelector('#deleteModal #quantity').value)
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
            }

            shoppingList.appendChild(li);
        });
        loadIcons()
        document.querySelector('#id').textContent = localStorage.getItem(this.hash + "_id");
        if (document.querySelector('#sharing-link-id')) document.querySelector('#sharing-link-id').remove()
    }
}

const addItemForm = document.getElementById('addItemForm');
addItemForm.addEventListener('submit', e => {
    e.preventDefault();

    const itemInput = document.getElementById('item');
    const newItem = itemInput.value.trim();

    let quantity = document.getElementById('quantity').value
    if (quantity === '') quantity = 1
    else if (quantity === 0) return
    else quantity = parseInt(quantity)

    if (newItem !== '') {
        console.log(activeList.getHash())

        activeList.add(newItem, quantity);
        itemInput.value = '';

        const list_name = activeList.getHash()
        postReq(
            'http://localhost:6969/req/addToList',
            {list_id: activeList.getId(), item_name: newItem, quantity: quantity}
        ).then(
            r => {
                if (!r) return

                localStorage.setItem(`changelog_${list_name}`, []);
                if (activeList.getHash() === list_name)
                    activeList.clearChangelog()
            },
            () => {
            }
        )
    }
});

document.querySelector('#sharingButton').addEventListener('click', function() {
    if (!document.querySelector('#sharing-link-id')) {
        const link = document.createElement('span')
        link.id = "sharing-link-id"
        link.textContent = `${window.location.protocol}//${window.location.host}/home?sharedList=${document.querySelector('#id').textContent}`
        document.querySelector('#sharing-id').appendChild(link)
    }
})



if (window.location.href.includes('sharedList')) {
    const newList = window.location.href.split('=')[1]
    postReq(
        'http://localhost:6969/req/createList',
        {list_name: newList}
    ).then(
        json => {
            if (json["status"] === 'existing') {
                lists.addSharedList(json['data'])
            } else if (json['status'] === 'created') {
                localStorage.setItem(newList + "_id", json['data']['list_id'])
                activeList = new ShoppingList(activeList.getHash())
            } else {
                console.log("Unknown status!")
            }
        }
    )
}
/**
 *
 *
 *
 **/
activeList = new ShoppingList(lists.getFirst())