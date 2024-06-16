<template>
  <div>
      <h2 class="contributors">Contributors</h2>
      <label class="container" style="margin-bottom: 25px; font-size: medium;">
          Select All
          <input type="checkbox" :checked="areAllSelected" @change="selectAll">
          <span class="checkmark"></span>
      </label>
      <label v-for="(username, index) in usernames" :key="index" class="container">
          {{ username }}
          <input type="checkbox" v-model="checkedUsers[index]">
          <span class="checkmark"></span>
      </label>
  </div>
</template>


<script>
export default {
    name: 'CheckBox',
    props: {
        usernames: {
            type: Array,
            required: true
        }
    },
    emits: ['update:selected'],
    data() {
        return {
            checkedUsers: this.usernames.map(() => true) // Initialize all users as checked
        }
    },
    methods: {
      selectAll(event) {
          const isChecked = event.target.checked;
          this.checkedUsers.fill(isChecked);
      },
      emitSelectedUsers() {
          const selectedUsernames = this.usernames.filter((_, index) => this.checkedUsers[index]);
          this.$emit('update:selected', selectedUsernames);
      }
    },
    watch: {
        usernames: {
            immediate: true,
            handler(newVal) {
                this.checkedUsers = newVal.map(() => true);
            }
        },
        checkedUsers: {
            deep: true,  // Necessary for watching array changes
            handler() {
                this.emitSelectedUsers();
            }
        }
    },
    computed: {
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