<!-- Copyright 2024 Radboud University, Modern Software Development Techniques

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. -->

<template>
    <grid-layout :layout.sync="layout"
                :col-num="12"
                :row-height="30"
                :is-draggable="draggable"
                :is-resizable="resizable"
                :vertical-compact="true"
                :use-css-transforms="true"
    >
        <grid-item v-for="item in layout"
                    :static="item.static"
                    :x="item.x"
                    :y="item.y"
                    :w="item.w"
                    :h="item.h"
                    :i="item.i"
        >
            <span class="text">{{itemTitle(item)}}</span>
        </grid-item>
    </grid-layout>
</template>

<script>
import { GridLayout, GridItem } from "vue-grid-layout"

export default {
components: {
    GridLayout,
    GridItem
},
data() {
    return {
        // The layout of the grid items.
        layout: [
            {"x":0,"y":0,"w":2,"h":2,"i":"0", static: false},
            {"x":2,"y":0,"w":2,"h":4,"i":"1", static: true},
            {"x":4,"y":0,"w":2,"h":5,"i":"2", static: false},
            {"x":6,"y":0,"w":2,"h":3,"i":"3", static: false},
            {"x":8,"y":0,"w":2,"h":3,"i":"4", static: false},
            {"x":10,"y":0,"w":2,"h":3,"i":"5", static: false},
            {"x":0,"y":5,"w":2,"h":5,"i":"6", static: false},
            {"x":2,"y":5,"w":2,"h":5,"i":"7", static: false},
            {"x":4,"y":5,"w":2,"h":5,"i":"8", static: false},
            {"x":6,"y":3,"w":2,"h":4,"i":"9", static: true},
            {"x":8,"y":4,"w":2,"h":4,"i":"10", static: false},
            {"x":10,"y":4,"w":2,"h":4,"i":"11", static: false},
            {"x":0,"y":10,"w":2,"h":5,"i":"12", static: false},
            {"x":2,"y":10,"w":2,"h":5,"i":"13", static: false},
            {"x":4,"y":8,"w":2,"h":4,"i":"14", static: false},
            {"x":6,"y":8,"w":2,"h":4,"i":"15", static: false},
            {"x":8,"y":10,"w":2,"h":5,"i":"16", static: false},
            {"x":10,"y":4,"w":2,"h":2,"i":"17", static: false},
            {"x":0,"y":9,"w":2,"h":3,"i":"18", static: false},
            {"x":2,"y":6,"w":2,"h":2,"i":"19", static: false}
        ],
        draggable: true,
        resizable: true,
        index: 0
    }
},
methods: {
    /**
     * Returns the title for a given item. If the item is static, appends " - Static" to the title.
     *
     * @param {Object} item - The grid item object.
     * @returns {String} The title of the item.
     */
    itemTitle(item) {
    let result = item.i;
    if (item.static) {
        result += " - Static";
    }
    return result;
    }
}
}
</script>

<style scoped>
.vue-grid-layout {
background: #eee;
}

.vue-grid-item:not(.vue-grid-placeholder) {
background: #ccc;
border: 1px solid black;
}

.vue-grid-item .resizing {
opacity: 0.9;
}

.vue-grid-item .static {
background: #cce;
}

.vue-grid-item .text {
font-size: 24px;
text-align: center;
position: absolute;
top: 0;
bottom: 0;
left: 0;
right: 0;
margin: auto;
height: auto;
width: 100%;
}

.vue-grid-item .no-drag {
height: auto;
width: 100%;
}

.vue-grid-item .minMax {
font-size: 12px;
}

.vue-grid-item .add {
cursor: pointer;
}

.vue-draggable-handle {
position: absolute;
width: 20px;
height: 20px;
top: 0;
left: 0;
background: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10'><circle cx='5' cy='5' r='5' fill='#999999'/></svg>") no-repeat;
background-position: bottom right;
padding: 0 8px 8px 0;
background-repeat: no-repeat;
background-origin: content-box;
box-sizing: border-box;
cursor: pointer;
}
</style>
