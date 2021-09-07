import React, {Component} from 'react';

class Navbar extends Component {
    constructor(props) {
        super(props);
        this.state = {menuMap: {}}
    }

    compileSubMenu(parent_id) {
        for (let subMenu of this.props.menu) {
            if (subMenu.parent === parent_id) {
                return
            }
        }
    }

    mapMenu() {
        const menuMap = {...this.state.menuMap}
        for (let menu of this.props.menu) {
            if (menu.parent == null) {
                menuMap[menu.id] = []
            } else {
                menuMap[menu.parent.id].push(menu.id)
            }
        }
        this.setState({menuMap: menuMap})
    }

    hasChildren(menu) {
        return this.state.menuMap[menu.id] !== undefined && this.state.menuMap[menu.id].length !==0
    }

    compileMenu(menu, index) {
        if (menu.parent == null) {
            if (this.hasChildren(menu)) {
                return (
                    <li key={index} className="nav-item dropdown">
                        <a className="nav-link dropdown-toggle" href="#" id={menu.name} role="button"
                           data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            {menu.name}
                        </a>
                        <div className="dropdown-menu" aria-labelledby={menu.name}>
                            {this.state.menuMap[menu.id].map((subMenu,subIndex)=>{
                                return <a key={subIndex} className="dropdown-item" href="#">{this.getSubMenu(subMenu)}</a>
                            })}
                        </div>
                    </li>
                )
            } else {
                return (
                        <li key={index} className="nav-item active">
                            <a className="nav-link" href="#">{menu.name} <span className="sr-only"/></a>
                        </li>
                )
            }

        }
    }

    getSubMenu(subMenu){
        for (let menu of this.props.menu){
            if (menu.id===subMenu) return menu.name
        }
    }
    render() {
        if (this.props.menu.length === 0) return null
        return (
            <nav className='navbar navbar-expand-lg navbar-light bg-light'>
                <a className="navbar-brand" href="#">something</a>
                <button className="navbar-toggler" type="button" data-toggle="collapse"
                        data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent"
                        aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"/>
                </button>

                <div className="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul className="navbar-nav mr-auto">
                        {this.props.menu.map((menu, index) => {
                            return this.compileMenu(menu, index)
                        })}
                    </ul>
                    <form className="form-inline my-2 my-lg-0">
                        <input className="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search"/>
                        <button className="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
                    </form>
                </div>
            </nav>
        );
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (this.props.menu.length === 0 || (prevProps.menu !== [] && prevProps.menu === this.props.menu)) return null
        this.mapMenu()
    }
}

export default Navbar;