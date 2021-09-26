import React, {Component} from 'react';
import {Link, BrowserRouter as Router} from "react-router-dom";

class Navbar extends Component {

    constructor(props) {
        super(props);
        this.logUserOut = this.logUserOut.bind(this)
    }


    logUserOut() {
        localStorage.removeItem('user')
        localStorage.setItem('isUserLoggedIn', "0")
        this.props.handleStatus(false)
    }



    render() {
        if (localStorage.getItem('isUserLoggedIn') === "1") {


        }
        if (this.props.menu.length === 0) return null
        return (
            <nav className='navbar navbar-expand-lg navbar-light bg-light'>
                <Link className="navbar-brand" to='#'>something</Link>
                <button className="navbar-toggler" type="button" data-toggle="collapse"
                        data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent"
                        aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"/>
                </button>

                <div className="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul className="navbar-nav ">
                        {this.props.menu.map((menu, index) => {
                            return this.compileMenu(menu, index)
                        })}
                        {this.generateAccount()}
                    </ul>
                    <form className="form-inline my-2 my-lg-0 mr-auto">
                        <input className="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search"/>
                        <button className="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
                    </form>
                    <Link className='btn btn-primary' to="#">ناحیه کاربری</Link>
                </div>
            </nav>
        );
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (this.props.menu.length === 0 || (prevProps.menu !== [] && prevProps.menu === this.props.menu)) return null

    }

    compileMenu(menu, index) {
        if (this.props.submenu[menu.id] !== undefined && this.props.submenu[menu.id].length > 0) {
            return (
                <li key={index} className="nav-item dropdown">
                    <a className="nav-link dropdown-toggle" href="#" id={`navbarDropdown${index}`} role="button"
                       data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        {menu.name}
                    </a>
                    <div className="dropdown-menu" aria-labelledby={`navbarDropdown${index}`}>
                        {this.props.submenu[menu.id].map((submenu, index) => {
                            return <Link key={index} className="dropdown-item" to={`/category/${submenu.id}`}>{submenu.name}</Link>
                        })}

                    </div>
                </li>
            )
        } else {
            return (
                <li key={index} className="nav-item">
                    <Link className="nav-link" to={`/category/${menu.id}`} >{menu.name}</Link>
                </li>
            )
        }
    }

    generateAccount() {
        if (this.props.loggedIn) {
            return (
                <li className="nav-item dropdown">
                    <a className="nav-link dropdown-toggle" href="#" id='navbarDropdown-account' role="button"
                       data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        ناحیه کاربری
                    </a>
                    <div className="dropdown-menu" aria-labelledby='navbarDropdown-account'>
                        <Link to="#" className="dropdown-item">اطلاعات کاربری</Link>
                        <Link to="#" onClick={this.logUserOut} className="dropdown-item">خروج</Link>
                    </div>
                </li>
            )
        } else {
            return (
                <li className="nav-item dropdown">
                    <a className="nav-link dropdown-toggle" href="#" id='navbarDropdown-account' role="button"
                       data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        ناحیه کاربری
                    </a>
                    <div className="dropdown-menu" aria-labelledby='navbarDropdown-account'>
                        <Link to="/login" className="dropdown-item">ورود</Link>
                        <Link to="/register" className="dropdown-item">ثبت نام</Link>
                    </div>
                </li>
            )
        }
    }
}

export default Navbar;