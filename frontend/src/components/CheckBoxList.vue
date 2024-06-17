<template>
  <div>
      <h2 class="contributors">Contributors</h2>
      <label class="container" style="margin-bottom: 25px; font-size: medium;">
          Select All
          <input type="checkbox" :checked="areAllSelected" @change="selectAll">
          <span class="checkmark"></span>
      </label>
      <div style="overflow-y: auto; max-height: 350px;">
        <label v-for="(username, index) in usernames" :key="index" class="container">
            {{ username }}
            <input type="checkbox" v-model="checkedUsers[index]">
            <span class="checkmark"></span>
        </label>
      </div>
  </div>
</template>

<script>
export default {
    name: 'CheckBox',
    props: {
        /**
         * Array of usernames to be displayed as checkbox options.
         * @type {Array}
         * @required
         */
        usernames: {
            type: Array,
            required: true
        }
    },
    emits: ['update:selected'],
    data() {
        return {
            /**
             * Array of booleans representing the checked state of each user.
             * @type {Array}
             */
            checkedUsers: this.usernames.map(() => true) // Initialize all users as checked
        }
    },
    methods: {
        /**
         * Selects or deselects all checkboxes based on the event target's checked state.
         * 
         * @param {Event} event - The change event triggered by the "Select All" checkbox.
         */
        selectAll(event) {
            const isChecked = event.target.checked;
            this.checkedUsers.fill(isChecked);
        },
        /**
         * Emits the list of selected usernames.
         */
        emitSelectedUsers() {
            const selectedUsernames = this.usernames.filter((_, index) => this.checkedUsers[index]);
            this.$emit('update:selected', selectedUsernames);
        }
    },
    watch: {
        /**
         * Watches for changes in the usernames prop and updates the checkedUsers array accordingly.
         * 
         * @param {Array} newVal - The new array of usernames.
         */
        usernames: {
            immediate: true,
            handler(newVal) {
                this.checkedUsers = newVal.map(() => true);
            }
        },
        /**
         * Watches for changes in the checkedUsers array and emits the selected users.
         */
        checkedUsers: {
            deep: true,  // Necessary for watching array changes
            handler() {
                this.emitSelectedUsers();
            }
        }
    },
    computed: {
        /**
         * Computed property to determine if all checkboxes are selected.
         * 
         * @returns {Boolean} True if all checkboxes are selected, false otherwise.
         */
        areAllSelected() {
            return this.checkedUsers.length && this.checkedUsers.every(Boolean);
        }
    }
}
</script>

<style scoped>
/* Customize the label (the container) */
.container {
  display: block;
  position: relative;
  padding-left: 35px;
  margin-bottom: 12px;
  cursor: pointer;
  font-size: 12px;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

/* Hide the browser's default checkbox */
.container input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

/* Create a custom checkbox */
.checkmark {
  position: absolute;
  top: 0;
  left: 0;
  height: 25px;
  width: 25px;
  background-color: #eee;
}

/* On mouse-over, add a grey background color */
.container:hover input ~ .checkmark {
  background-color: #ccc;
}

/* When the checkbox is checked, add a blue background */
.container input:checked ~ .checkmark {
  background-color: #2196F3;
}

/* Create the checkmark/indicator (hidden when not checked) */
.checkmark:after {
  content: "";
  position: absolute;
  display: none;
}

/* Show the checkmark when checked */
.container input:checked ~ .checkmark:after {
  display: block;
}

/* Style the checkmark/indicator */
.container .checkmark:after {
  left: 9px;
  top: 5px;
  width: 5px;
  height: 10px;
  border: solid white;
  border-width: 0 3px 3px 0;
  -webkit-transform: rotate(45deg);
  -ms-transform: rotate(45deg);
  transform: rotate(45deg);
}

/* Title */
.contributors {
  font-size: 20px;
  margin-bottom: 20px;
}
</style>
