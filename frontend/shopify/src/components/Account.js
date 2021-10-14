import React, {Component} from 'react';
import Address from "./Address";

class Account extends Component {
    state = {
        address: [],
        first_name:"",
        last_name:""
    }
    getOrderHistory = (howmuch = false) => {
        if (howmuch) {
            const url = ""
        }
    }
    handleInputAddress = ({currentTarget: input}) => {
        this.setState({address: input.value})
    }
    updateUserForm = (data) => {
        if (this.state.first_name !== data.first_name && this.state.last_name !== data.last_name){
            this.setState({first_name: data.first_name, last_name: data.last_name})
        }

    }
    updateAddress =(data)=>{
        this.setState({address:data})
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
        fetch(address_url, option).then(response => response.json()).then(data => this.updateAddress(data))
    }
    render() {
        return (
            <div>
                <nav>
                    <div className="nav nav-tabs" id="nav-tab" role="tablist">
                        <a className="nav-link active" id="nav-home-tab" data-toggle="tab" href="#nav-home" role="tab"
                           aria-controls="nav-home" aria-selected="true">اطلاعات کاربری</a>
                        <a className="nav-link" id="nav-contact-tab" data-toggle="tab" href="#nav-contact" role="tab"
                           aria-controls="nav-contact" aria-selected="false">پیشینه سفارشات</a>
                    </div>
                </nav>
                <div className="tab-content" id="nav-tabContent">
                    <div className="tab-pane fade show active" id="nav-home" role="tabpanel"
                         aria-labelledby="nav-home-tab">

                        <form>
                            <div className="form-group">
                                <label htmlFor="fist_name">
                                    نام:
                                </label>
                                <input type="text" name="first_name"/>
                                <label htmlFor="last_name">
                                    نام خانوادگی:
                                </label>
                                <input type="text" name="last_name"/>
                                {this.state.address && this.state.address.map((address,index)=>{
                                    return <h1>hi</h1>
                                })}
                            </div>
                            <div className='form-group'>

                            </div>
                        </form>

                    </div>

                    <div className="tab-pane fade" id="nav-contact" role="tabpanel"
                         aria-labelledby="nav-contact-tab">...
                    </div>
                </div>

            </div>
        );
    }
    componentDidMount() {
        this.getInfo()
    }
}

export default Account;