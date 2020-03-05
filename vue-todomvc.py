<!doctype html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Template • TodoMVC</title>
    <!-- 样式文件 -->
    <link rel="stylesheet" href="node_modules/todomvc-common/base.css">
    <link rel="stylesheet" href="node_modules/todomvc-app-css/index.css">
    <link rel="stylesheet" href="css/app.css">
</head>

<body>
    <section class="todoapp">
        <!-- vue组件 -->
        <todo-header @add-todo="addTodo"></todo-header>
        <todo-main @checked-all="checkedAll" @checked-status="checkedStatus" @edit-todo="editTodo" @del-todo="delTodo"
            :selected="selected" :list="list"></todo-main>
        <todo-footer @clear-todo="clearTodo" @edit-state="editState" :selected="selected" :list="list"></todo-footer>
    </section>

    <!-- 引入vue -->
    <script src="./node_modules/vue/dist/vue.js"></script>

    <script src="node_modules/todomvc-common/base.js"></script>
    <!-- 拆分的头部子组件、主体子组件、底部子组件以及父组件 -->
    <script src="js/header.js"></script>
    <script src="js/main.js"></script>
    <script src="js/footer.js"></script>
    <script src="js/app.js"></script>
</body>

</html>
==================JS-header部分=====================

Vue.component('todo-header', {
  template: `
  <header class="header">
    <h1>todos</h1>
    <input @keyup.enter="addTodo" class="new-todo" placeholder="What needs to be done?">
  </header>
  `,
  methods: {
    //添加土豆
    addTodo(e) {
      //非空
      if (e.target.value == '') {
        return
      }
      // console.log(e.target.value);
      //将input中的内容传给父组件，由父组件添加
      this.$emit('add-todo', e.target.value)
      e.target.value = ''
    }
  }
})
==================JS-main部分=====================

Vue.component('todo-main', {
  template: `
        <section class="main">
            <input v-model="isCheckedAll" id="toggle-all" class="toggle-all" type="checkbox">
            <label for="toggle-all">Mark all as complete</label>
            <ul class="todo-list">
                <li v-for="item in showList" :for="item.id" :class="{completed:item.flag,editing:item.id==edit}">
                    <div class="view">
                        <input @click="checkedStatus(item.id)" class="toggle" type="checkbox" :checked="item.flag">
                        <label @dblclick="showEdit(item.id)">{{item.name}}</label>
                        <button @click="delTodo(item.id)" class="destroy"></button>
                    </div>
                    <input @keyup.enter="editTodo" class="edit" :value="item.name">
                </li>
            </ul>
        </section>
    `,
  //接收父组件传递过来的数据
  props: ['list', 'selected'],
  data() {
    return {
      edit: -1
    }
  },
  methods: {
    //删除土豆
    delTodo(id) {
      // console.log(id);
      //将被点击的按钮对应的id传给父组件，由父组件删除
      this.$emit('del-todo', id)
    },
    //显示修改任务的input框
    showEdit(id) {
      this.edit = id
    },
    //将修改任务的input对应的id及修改后input的内容传给父组件，由父组件修改
    editTodo(e) {
      this.$emit('edit-todo', this.edit, e.target.value)
      this.edit = -1
    },
    //获取点击的checkbox的id传给父组件
    checkedStatus(id) {
      // console.log(id);
      this.$emit('checked-status', id)
    }
  },
  computed: {
    //全选及全不选功能
    isCheckedAll: {
      //如果下边的checkbox都被选中那么上边的高亮
      get() {
        return this.list.every(v => v.flag)
      },
      //上边的高亮状态控制下边checkbox是否被选中，由父组件控制
      set(value) {
        // console.log(value);
        this.$emit('checked-all', value)
      }
    },
    //不能直接更改父组件的list数据，克隆一份一模一样的
    showList() {
      if (this.selected == 'active') {
        return this.list.filter(v => !v.flag)
      } else if (this.selected == 'completed') {
        return this.list.filter(v => v.flag)
      } else {
        return this.list
      }
    }
  },

})