/**
 * @fileOverview Offline managment of the application
 * @description This script manages a simple shopping list application with features like creating, renaming, deleting, and syncing lists. It uses local storage for data persistence and allows sharing lists via generated links.
 * @version 1.0.0
 * @license MIT License
 */

/**
 * Represents the currently active shopping list.
 * @type {ShoppingList}
 */
let activeList = null;

/**
 * Flag indicating whether the application is disconnected from the cloud.
 * @type {boolean}
 */
let disconnectFromCloud = false;

/**
 * Adds a overlay when content is loading
 */
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

/**
 * Manages the side menu functionality.
 * @function
 */
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

/**
 * Adds mouseover and mouseleave event listeners to icons for visual effects.
 * @function
 */
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

/**
 * Wrapper that creates a shopping list item with a name and quantity.
 * @function
 * @param {string} name - The name of the item.
 * @param {number} quantity - The quantity of the item.
 * @returns {Object} - The created item object.
 */
function createItem(name, quantity) {
    return {
        'name': name,
        'quantity': quantity
    }
}

/**
 * Adds a timeout to a Promise, rejecting it with an error if it takes too long to resolve or reject.
 *
 * @param {number} ms - The maximum time allowed for the Promise to resolve or reject, in milliseconds.
 * @param {Promise} promise - The Promise to be wrapped with a timeout.
 * @returns {Promise} - Promise to evaluate that either resolves with the original value of the provided Promise
 *                     or rejects with an error indicating a timeout.
 * @throws {Error} - If the provided promise takes longer than the specified timeout duration.
 */
function timeout(ms, promise) {
    return new Promise((resolve, reject) => {
        const timer = setTimeout(() => {
            reject(new Error('Request timeout'))
        }, ms)

        promise.then(value => {
            clearTimeout(timer)
            resolve(value)
        })
        .catch(reason => {
            clearTimeout(timer)
            reject(reason)
        })
    })
}

/**
 * Sends a POST request to the specified URL with JSON data.
 * @async
 * @function
 * @param {string} url - The URL for the POST request.
 * @param {Object} data - The data to be sent in the request body.
 * @returns {Promise<Object>} - A Promise that resolves to the JSON response.
 */
async function postReq(url, data) {
    if (disconnectFromCloud) throw "Disconnected from cloud";

    try {
        const response = await timeout(3500, fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        }));
        return await response.json();
    } catch (error) {
        console.error('Error during POST request:', error);
        disconnectFromCloud = true 
        document.getElementById('disconnect-icon').classList.toggle('d-none', false)
        document.getElementById('helper_disc').textContent = 'Connect to cloud'
        return ''
    }
}

/**
 * MD5 hash function for generating hash values.
 * @function
 * @param {string} d - The input string to be hashed.
 * @returns {string} - The MD5 hash value.
 */
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

async function areyouthere(){
    await timeout(2000, fetch(`http://localhost:6969/req/areyouthere`)).then(
        _ => {
            disconnectFromCloud = false
            document.getElementById('disconnect-icon').classList.toggle('d-none', true)
            document.getElementById('helper_disc').textContent = 'Disconnect from cloud'
        }
    ).catch(
        _ => {
            disconnectFromCloud = true
            document.getElementById('disconnect-icon').classList.toggle('d-none', false)
            document.getElementById('helper_disc').textContent = 'Connect to cloud'
        }
    )
}

/**
 * Synchronizes the active shopping list with the cloud.
 * @async
 * @function
 */
async function cloudSync() {
    await areyouthere()
    if(disconnectFromCloud) return

    let lists_to_delete = JSON.parse(localStorage.getItem('lists_to_delete'))
    if(lists_to_delete){
        for(let l of lists_to_delete){
            postReq(
                'http://localhost:6969/req/removeList',
                { list_id: l }
            ).then(
                response => { 
                    if(response != '') onListDeleted(l) 
                }
            )
        }
    }

    // We arent inside a list
    if (!activeList.getName()) return

    // The list has a ID? (it doesnt has a ID if never got syncronized)
    if (activeList.getId()) {
        let response = await fetch(`http://localhost:6969/req/cloudHash/${activeList.getId()}`)
        let cloudHash = await response.text()
        let localHash = MD5(`{list_name:${activeList.name.replaceAll(' ', '').replace(/\([^)]*\)/g, '').trim()},items:${JSON.stringify(activeList.items).replaceAll('\"', '')}}`)

        if (cloudHash == localHash) {
            console.log('shopping list is syncronized.')
            document.getElementById("sync-overlay").classList.toggle('d-none', true)
            return
        }

        console.log('shopping list not syncronized, requesting the cloud.')
        document.getElementById("sync-overlay").classList.toggle('d-none', false)
        response = await postReq(
            `http://localhost:6969/req/synchronize/${activeList.getId()}`,
            activeList.changes
        )

        if(response === ''){
            document.getElementById("sync-overlay").classList.toggle('d-none', true)   
            return
        }

        // The list got deleted
        if(!response['items']){
            localStorage.removeItem(`${activeList.getName()}_id`);
            lists.delete(activeList.getName())
            document.getElementById("sync-overlay").classList.toggle('d-none', true)
            return
        }

        localStorage.setItem(activeList.getName() + "_id", response['id'])
        localStorage.setItem(`changelog_${response['list_name']}`, [])
        localStorage.setItem(activeList.getName(), JSON.stringify(response['items']));

        document.getElementById('id').textContent = response['id']

        activeList = new ShoppingList(activeList.getName())
        lists.render()
    } else {
        console.log('shopping list doesnt exists in the cloud, creating...')
        document.getElementById("sync-overlay").classList.toggle('d-none', false)
        const response = await postReq(
            `http://localhost:6969/req/synchronize/${activeList.getId()}`,
            {
                'name': activeList.getName(),
                'changes': activeList.changes
            }
        )

        if(response === ''){
            document.getElementById("sync-overlay").classList.toggle('d-none', true)   
            return
        }

        localStorage.setItem(response['list_name'] + "_id", response['id'])
        localStorage.setItem(`changelog_${response['list_name']}`, [])
        activeList = new ShoppingList(activeList.getName())

        document.getElementById('id').textContent = response['id']
    }

    document.getElementById("sync-overlay").classList.toggle('d-none', true)
}

function cacheListToDelete(name){
    let lists = JSON.parse(localStorage.getItem('lists_to_delete'))
    if(lists == null) lists = []
    lists.push(name)
    localStorage.setItem('lists_to_delete', JSON.stringify(lists))
}

function onListDeleted(name){
    const lists = JSON.parse(localStorage.getItem('lists_to_delete'))
    for (let i = 0; i < lists.length; i++) {
        if (lists[i] == name) {
            index = i;
            break;
        }
    }
    localStorage.setItem('lists_to_delete', JSON.stringify(lists.splice(index, 1)))
}

/**
 * Gets the current timestamp in seconds.
 * @function
 * @returns {number} - The timestamp in seconds.
 */
function getTimestampInSeconds() {
    const date = new Date();
    return Math.floor(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate(), date.getHours(), date.getMinutes(), date.getSeconds()) / 1000);
}

/**
 * Interval function for continuous cloud synchronization
 * @function
 */
setInterval(() => {
    cloudSync()
}, 5000);

/**
 * Helper function that clear local storage
 * @function
 */
document.getElementById('helper_clear').addEventListener('click', () => {
    localStorage.clear()
    location.reload()
})

/**
 * Helper manual sync
 * @function
 */
document.getElementById('helper_sync').addEventListener('click', cloudSync)

/**
 * Helper that disconnects from the cloud
 * @function
 */
document.getElementById('helper_disc').addEventListener('click', () => {
    if (disconnectFromCloud)
        document.getElementById('helper_disc').textContent = 'Disconnect from cloud'
    else
        document.getElementById('helper_disc').textContent = 'Connect to cloud'

    document.getElementById('disconnect-icon').classList.toggle('d-none', disconnectFromCloud)
    disconnectFromCloud = !disconnectFromCloud
})

/**
 * Represents a collection of shopping lists.
 * @class
 */
class ShoppingLists {
    /**
     * Initializes the class by loading existing shopping lists and rendering them.
     */
    constructor() {
        this.lists = this.load();
        this.render();
    }

    /**
     * Retrieves shopping lists from local storage or initializes an empty array if none exists.
     * @returns {Array} - The array of shopping lists.
     */
    load() {
        const list = localStorage.getItem('shoppingLists');
        return list ? JSON.parse(list) : [];
    }

    /**
     * Adds a shared list to the collection and performs necessary local storage and synchronization actions.
     * @param {Object} list - The shared list object received from the cloud.
     */
    addSharedList(list) {
        const name = list['list_name'] + ` (${list['email']})`;
        const existingList = localStorage.getItem(name);

        if (existingList) return;

        this.lists.push(name);
        localStorage.setItem(name, JSON.stringify(list['items']));
        localStorage.setItem(name + "_id", list['id']);
        localStorage.setItem(`changelog_${name}`, []);

        activeList = new ShoppingList(name);
        this.save();
        cloudSync();
    }

    /**
     * Persists the current state of the shopping lists to local storage and triggers a render.
     */
    save() {
        localStorage.setItem('shoppingLists', JSON.stringify(this.lists));
        this.render();
    }

    /**
     * Creates a new shopping list with the given name and optional list ID.
     * @param {string} name - The name of the new shopping list.
     * @param {string} list_id - This value should come from the cloud
     */
    create(name, list_id) {
        const existingList = localStorage.getItem(name);
        if (existingList) return;

        this.lists.push(name);
        localStorage.setItem(name, []);
        if (list_id) localStorage.setItem(name + "_id", list_id);

        activeList = new ShoppingList(name);
        this.save();
    }

    /**
     * Deletes a shopping list from the collection and performs necessary local storage and synchronization actions.
     * @param {string} item - The name of the shopping list to be deleted.
     * @param {number} index - The optional index of the shopping list in the collection.
     */
    delete(item, index) {
        if (index === undefined) {
            for (let i = 0; i < this.lists.length; i++) {
                if (this.lists[i] === item) {
                    index = i;
                    break;
                }
            }
        }
        this.lists.splice(index, 1);

        // It exists in the cloud?
        const list_id = localStorage.getItem(`${item}_id`)
        if(list_id){
            // In case the cloud doesn't responds
            cacheListToDelete(list_id)
    
            postReq(
                'http://localhost:6969/req/removeList',
                { list_id: list_id }
            ).then(
                response => { 
                    if(response != '') onListDeleted(list_id) 
                }
            )
        }

        localStorage.removeItem(item);
        localStorage.removeItem(`changelog_${item}`);
        localStorage.removeItem(`${item}_id`);

        if (activeList.getName() === item)
            activeList = new ShoppingList(this.getFirst());

        this.save();
    }

    /**
     * Renders the shopping lists in the user interface
     */
    render() {
        const ul = document.getElementById('others');
        ul.innerHTML = '';

        this.lists.forEach((item, index) => {
            const cache = localStorage.getItem(item);
            const list = cache !== '' ? JSON.parse(cache) : [];
            const quantity = list.reduce((acc, val) => val.quantity > 0 ? acc + val.quantity : acc, 0);

            const li = document.createElement('li');
            li.classList = 'px-3 w-100 d-flex justify-content-between align-items-center';
            li.innerHTML = `
                <span>${item}</span>
                <div class="d-flex gap-2 align-items-center">
                    <span class="badge bg-primary rounded-pill">${quantity}</span>
                    <i class="fa-solid fa-delete-left whiteIcon"></i>
                </div>
            `;

            li.querySelector('span').addEventListener('click', () => {
                activeList = new ShoppingList(item);
            });

            li.querySelector('i').addEventListener('click', e => {
                e.preventDefault();
                this.delete(item, index);
            });

            ul.appendChild(li);
        });
        loadIcons();
    }

    /**
     * Retrieves the name of the first shopping list in the collection, if any.
     * @returns {string|null} - The name of the first shopping list or null if the collection is empty.
     */
    getFirst() {
        return this.lists.length === 0 ? null : this.lists[0];
    }
}

/**
 * Instance that manages all lists
 */
const lists = new ShoppingLists()

/**
 * Event listener for the creating of a new list
 */
const addListForm = document.getElementById('addListForm');
addListForm.addEventListener('submit', async e => {
    e.preventDefault();

    const input = document.getElementById('list');
    const newList = input.value.replace(/[^a-zA-Z ]/g, '').trim();

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
                    activeList = new ShoppingList(activeList.getName())
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
 * Represents an individual shopping list.
 * @class
 */
class ShoppingList {
    /**
     * Initializes the shopping list based on the provided name.
     * If the name is null, displays a message indicating the absence of lists.
     * @param {string} name - Shopping list name
     */
    constructor(name) {
        if (name == null) {
            document.querySelector('h3').innerHTML = `You don't have any lists, please create one.`;
            document.getElementById('shoppingList').innerHTML = '';
            document.getElementById('id').innerHTML = '';
            if (document.querySelector('#sharing-link-id')) document.querySelector('#sharing-link-id').remove();
            document.querySelector('#formsWrapper').style.display = "none";
        } else {
            this.name = name;
            this.list_id = localStorage.getItem(name + "_id");
            this.items = this.load();
            this.changes = this.changelog();
            document.querySelector('#formsWrapper').style.display = "flex";
            this.render();
        }
    }

    /**
     * Clears the changelog for the shopping list.
     */
    clearChangelog() {
        this.changes = [];
    }

    /**
     * Retrieves the ID associated with the shopping list.
     * @returns {string|null} - The ID of the shopping list.
     */
    getId() {
        return this.list_id;
    }

    /**
     * Retrieves the name of the shopping list.
     * @returns {string} - The hash of the shopping list.
     */
    getName() {
        return this.name;
    }

    /**
     * Loads the items of the shopping list from local storage.
     * @returns {Array} - The array of items in the shopping list.
     */
    load() {
        const list = localStorage.getItem(this.name);
        return list ? JSON.parse(list) : [];
    }

    /**
     * Retrieves the changelog of the shopping list from local storage.
     * @returns {Array} - The array representing the changelog of the shopping list.
     */
    changelog() {
        const cl = localStorage.getItem(`changelog_${this.name}`);
        return cl ? JSON.parse(cl) : [];
    }

    /**
     * Logs an operation in the changelog of the shopping list.
     * @param {Object} info - The information about the operation to be logged.
     */
    log(info) {
        this.changes.push(info);
        localStorage.setItem(`changelog_${this.name}`, JSON.stringify(this.changes));
    }

    /**
     * Persists the current state of the shopping list to local storage and triggers a render of the lists.
     */
    save() {
        localStorage.setItem(this.name, JSON.stringify(this.items));
        lists.render();
    }

    /**
     * Modifies the shopping list based on the provided function, saves the changes, and triggers a render.
     * @param {Function} func - The function that modifies the shopping list.
     */
    modify(func) {
        func();
        this.save();
        this.render();
    }

    /**
     * Adds an item to the shopping list, updating quantity if the item already exists.
     * @param {string} item - The name of the item to be added.
     * @param {number} quantity - The quantity of the item to be added.
     */
    add(item, quantity) {
        if (this.items.map(i => i.name).includes(item)) {
            this.modify(() => {
                this.items.filter(i => i.name === item)[0].quantity += quantity;
            });
            this.log({'operation': 'add', 'item': item, 'quantity': quantity, 'timestamp': getTimestampInSeconds()});
        } else if (quantity > 0) {
            this.modify(() => {
                this.items.push(createItem(item, quantity));
            });
            this.log({'operation': 'add', 'item': item, 'quantity': quantity, 'timestamp': getTimestampInSeconds()});
        }
    }

    /**
     * Deletes an item from the shopping list, updating quantity and performing necessary synchronization.
     * @param {number} index - The index of the item to be deleted.
     * @param {number} quantity - The quantity of the item to be deleted.
     */
    delete(index, quantity) {
        const list_name = activeList.getName();
        postReq(
            'http://localhost:6969/req/buyItem',
            {list_id: activeList.getId(), name: this.items[index].name, quantity: quantity}
        ).then(
            r => {
                if (!r) return;

                localStorage.setItem(`changelog_${list_name}`, []);
                if (activeList.getName() === list_name)
                    activeList.clearChangelog();
            },
            () => {
            }
        );

        if (quantity < 1) return;

        this.log({
            'operation': 'buy',
            'item': this.items[index].name,
            'quantity': quantity,
            'timestamp': getTimestampInSeconds()
        });
        this.modify(() => {
            this.items[index].quantity -= quantity;
        });
    }

    /**
     * Renames an item in the shopping list, performing necessary synchronization if needed.
     * @param {Object} item - The item object to be renamed.
     * @param {string} newName - The new name for the item.
     */
    rename(item, newName) {
        if (newName === '' || item.name === newName) return;

        const list_name = activeList.getName();
        postReq(
            'http://localhost:6969/req/renameItem',
            {list_id: activeList.getId(), item_name: item.name, new_item_name: newName}
        ).then(
            r => {
                if (!r) return;

                localStorage.setItem(`changelog_${list_name}`, []);
                if (activeList.getName() === list_name)
                    activeList.clearChangelog();
            },
            () => {
            }
        );

        if (this.items.map(i => i.name).includes(newName)) {
            this.modify(() => {
                this.items.filter(i => i.name === newName)[0].quantity += item.quantity;
                this.items = this.items.filter(i => i.name !== item.name);
            });
            this.log({'operation': 'remove', 'item': item.name, 'timestamp': getTimestampInSeconds()});
            this.log({
                'operation': 'add',
                'item': newName,
                'quantity': item.quantity,
                'timestamp': getTimestampInSeconds()
            });
        } else {
            this.log({
                'operation': 'rename',
                'item': item.name,
                'newItem': newName,
                'timestamp': getTimestampInSeconds()
            });
            this.modify(() => {
                item.name = newName;
            });
        }
    }

    /**
     * Renders the shopping list in the user interface
     */
    render() {
        const shoppingList = document.getElementById('shoppingList');
        shoppingList.innerHTML = '';

        document.querySelector('h3').innerHTML = `List: ${this.name}`;

        const deleteModal = document.getElementById('deleteModal');
        const renameModal = document.getElementById('renameModal');

        this.items.forEach((item, index) => {
            const li = document.createElement('li');
            li.classList = 'px-3 w-100 d-flex justify-content-between align-items-center';
            li.style.height = "40px";
            if (item.quantity == 0) {
                li.innerHTML = `
                <span style="text-decoration: line-through;">${item.name}</span>
                <div class="d-flex gap-2 align-items-center">
                    <span class="badge bg-primary rounded-pill">${item.quantity}</span>
                </div>
            `;
            }
            else {
                li.innerHTML = `
                <span>${item.name}</span>
                <div class="d-flex gap-2 align-items-center">
                    <span class="badge bg-primary rounded-pill">${item.quantity}</span>
                    <button type="button" class="btn delete" data-bs-toggle="modal" data-bs-target="#deleteModal"><i class="fa-solid fa-cart-shopping blackIcon"></i></button>
                    <button type="button" class="btn rename" data-bs-toggle="modal" data-bs-target="#renameModal"><i class="fa-solid fa-font blackIcon"></i></button>
                </div>
            `;
                li.querySelector('button.delete').addEventListener('click', () => {
                    document.querySelector('#deleteModal #quantity').value = item.quantity;
                    let action = deleteModal.querySelector('.modal-action');
                    action.outerHTML = action.outerHTML; // reset listeners
                    action = deleteModal.querySelector('.modal-action');
                    action.addEventListener('click', () => {
                        this.delete(index, document.querySelector('#deleteModal #quantity').value);
                    });
                });

                li.querySelector('button.rename').addEventListener('click', () => {
                    document.getElementById('renameModalLabel').textContent = `Rename item: "${item.name}"`;

                    let action = renameModal.querySelector('.modal-action');
                    action.outerHTML = action.outerHTML; // reset listeners
                    action = renameModal.querySelector('.modal-action');
                    action.addEventListener('click', () => {
                        this.rename(item, document.getElementById('newName').value);
                    });
                });
            }

            shoppingList.appendChild(li);
        });
        loadIcons();
        document.querySelector('#id').textContent = localStorage.getItem(this.name + "_id");
        if (document.querySelector('#sharing-link-id')) document.querySelector('#sharing-link-id').remove();
    }
}

/**
 * Event listener for the creation of a new item
 */
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
        console.log(activeList.getName())

        activeList.add(newItem, quantity);
        itemInput.value = '';

        const list_name = activeList.getName()
        postReq(
            'http://localhost:6969/req/addToList',
            {list_id: activeList.getId(), item_name: newItem, quantity: quantity}
        ).then(
            r => {
                if (!r) return

                localStorage.setItem(`changelog_${list_name}`, []);
                if (activeList.getName() === list_name)
                    activeList.clearChangelog()
            },
            () => {
            }
        )
    }
});

/**
 * Event listener for the "click" event on the sharing button.
 */
document.querySelector('#sharingButton').addEventListener('click', function() {
    if (!document.querySelector('#sharing-link-id')) {
        const link = document.createElement('span')
        link.id = "sharing-link-id"
        link.textContent = `${window.location.protocol}//${window.location.host}/home?sharedList=${document.querySelector('#id').textContent}`
        document.querySelector('#sharing-id').appendChild(link)
    }
})

/**
 * Handles sharing lists by url
 */
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
                activeList = new ShoppingList(activeList.getName())
            } else {
                console.log("Unknown status!")
            }
        }
    )
}

/**
 * Initializes a list
 */
activeList = new ShoppingList(lists.getFirst())
areyouthere()