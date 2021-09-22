import './App.css';
import Navbar from "./components/Navbar";
import React, {Component} from 'react';
import {BrowserRouter as Router, Route, Link, Switch} from "react-router-dom";
import Category from "./components/Category";
import Register from "./components/Register";
import Login from "./components/Login";

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            menu: [],
            submenu: [],
            user: null,
            loggedIn: false,
            user_permission: ""
        }
        this.getMenu()
    }

    setStatus = (loginStatus) => {
        this.setState({loggedIn: loginStatus})
    }

    async getMenu() {
        await fetch('http://127.0.0.1:8000/category/roots/').then(response => response.json()).then(roots => this.generateMenuTree(roots))

    }

    async generateMenuTree(roots) {
        this.setState({menu: roots})
        for (let root of roots) {
            fetch(`http://127.0.0.1:8000/category/${root.id}/children/`).then(response => response.json()).then(submenu => this.fillMenuData(root.id, submenu))
        }
    }

    fillMenuData(root_id, submenu) {
        const menu = {...this.state.submenu}
        menu[root_id] = submenu
        this.setState({submenu: menu})
    }

    set_user_permission = (user_permission) =>{
        this.setState({user_permission:user_permission})
    }
    render() {

        return (

            <Router>
                <div>
                    <Navbar menu={this.state.menu} submenu={this.state.submenu} loggedIn={this.state.loggedIn}
                            handleStatus={this.setStatus} user_permission={this.state.user_permission}/>
                    <Switch>
                        <Route path="/register">
                            <Register handleStatus={this.setStatus} set_user_permission={this.set_user_permission}/>
                        </Route>
                        <Route path="/login">
                            <Login handleStatus={this.setStatus} set_user_permission={this.set_user_permission}/>
                        </Route>
                        <Route path="/category/:id">
                            <Category/>
                        </Route>
                    </Switch>
                </div>
            </Router>

        )
    }

    componentDidMount() {
        const user = localStorage.getItem('user')
        this.setState({user: user})
        if (localStorage.getItem('isUserLoggedIn') === "1") {
            this.setState({loggedIn: true})
        }
        if (localStorage.getItem('user_permission') !== undefined) {
            this.setState({user_permission: localStorage.getItem('user_permission')})
        }
    }
}

export default App;

