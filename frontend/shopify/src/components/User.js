import React, {Component} from 'react';
import Address from "./Address";

class User extends Component {
    state = {
        first_name: "",
        last_name: "",
        address: []
    }

    getInfo = () => {
        const option = {
            method: "GET",
            headers: {
                'Accept': 'application/json, text/plain',
                'Content-Type': 'application/json;charset=UTF-8',
                'Authorization': `token ${this.props.user ? this.props.user : localStorage.getItem('user')}`
            }
        }
        const token = localStorage.getItem('user')
        const url = `http://127.0.0.1:8000/account/auth/${token}/`
        fetch(url, option).then(response => response.json()).then(data => this.updateUserForm(data))
        const address_url = 'http://127.0.0.1:8000/account/address/'
        fetch(address_url, option).then(response => response.json()).then(data => this.updateAddressForm(data))
    }
    updateUserForm = (data) => {
        if (this.state.first_name !== data.first_name && this.state.last_name !== data.last_name){
            this.setState({first_name: data.first_name, last_name: data.last_name})
        }

    }
    updateAddressForm = (data) => {
        console.log(data)
        this.setState({address: data})
    }
    handleChange =({currentTarget: input})=>{
        this.setState({[input.id] : input.value})
    }
    render() {

        return (
            <div>
                <label htmlFor='first_name'>نام: </label>
                <input name='first_name' id='first_name' value={this.state.first_name} onChange={this.handleChange}/>
                <label htmlFor='last_name'>نام خانوادگی: </label>
                <input name='last_name' id='last_name' value={this.state.last_name} onChange={this.handleChange}/>
                <Address address ={this.state.address}/>

            </div>
        );
    }
    componentDidMount() {
        this.getInfo()
    }
}

export default User;