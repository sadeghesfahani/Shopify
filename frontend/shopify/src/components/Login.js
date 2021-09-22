import React, {Component} from 'react';
import {Redirect} from "react-router-dom";

class Login extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this)
    }

    state = {
        account: {
            email: "",
            password: ""
        },
        errors: {},
        redirect: false,
        loggedIn: localStorage.getItem('isUserLoggedIn')
    }

    handleChange = ({currentTarget: input}) => {
        const account = {...this.state.account}
        account[input.id] = input.value;
        this.setState({account})
    }

    async handleSubmit(e) {
        e.preventDefault()

        const result = await this.logIn()
        if (result['status']) {
            localStorage.setItem('user', result['token'])
            localStorage.setItem('isUserLoggedIn', "1")
            localStorage.setItem('user_permission',result['user_permission'])

            console.log("result")
            console.log(result)
            this.props.set_user_permission(result['user_permission'])
            this.props.handleStatus(true)
            this.setState({redirect: true})

        }
    }

    redirectToHome() {
        return <Redirect to='/'/>
    }

    prepareData = () => {
        const {account} = this.state
        return JSON.stringify({
            email: account.email,
            password: account.password
        })
    }

    async logIn() {

        const option = {
            method: "POST",
            body: this.prepareData(),
            headers: {
                'Accept': 'application/json, text/plain',
                'Content-Type': 'application/json;charset=UTF-8'
            }
        }
        const result = await fetch("http://127.0.0.1:8000/account/auth/login/", option)
        return await result.json()
    }

    render() {
        const {account} = this.state
        if(this.state.loggedIn === "1"){
            this.setState({redirect:true})
        }
        return (
            <div className='card w-50 text-right mx-auto mt-3'>
                {this.state.redirect && this.redirectToHome()}
                <div className='card-header'>
                    ثبت نام
                </div>
                <div className="card-body">
                    <form onSubmit={this.handleSubmit}>
                        <div className='form-group'>
                            <label htmlFor="email">ایمیل</label>
                            <input onChange={this.handleChange} value={account.email} type='email'
                                   className='form-control' id='email'/>
                            <label htmlFor="password">کلمه عبور</label>
                            <input onChange={this.handleChange} value={account.password} type='password'
                                   className='form-control' id='password'/>

                            <button type="submit" className="btn btn-primary">Submit</button>
                        </div>
                    </form>

                </div>
                <div className="card-footer">
                    this is buttom
                </div>
            </div>
        );
    }
}

export default Login;