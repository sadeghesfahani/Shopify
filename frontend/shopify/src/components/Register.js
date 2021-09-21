import React, {Component} from 'react';
import './Register.css';
import Joi from 'joi-browser'
import { Redirect } from "react-router-dom";

class Register extends Component {
    constructor(props) {

        super(props);
        this.handleSubmit = this.handleSubmit.bind(this)
        this.register = this.register.bind(this)
        this.state = {
            account: {
                email: "",
                password: "",
                re_password: ""
            },
            errors: {}
        }
    }

    schema = {
        email: Joi.string().email().required(),
        password: Joi.string().min(5).required(),
        re_password: Joi.string().min(5).required()

    }
    handleChange = ({currentTarget: input}) => {
        const account = {...this.state.account}
        account[input.id] = input.value;
        this.setState({account})
    }

    async handleSubmit(e) {
        e.preventDefault()
        const {account} = this.state
        this.validate()
        if (this.state.errors) {
            if (account.password === account.re_password) {
                console.log('also here')
                const result = await fetch(`http://127.0.0.1:8000/account/auth/is_user_exist/?email=${account.email}`)
                const response = await result.json()
                const exists = response['exists']
                if (!exists) {
                    const response = await this.register()
                    if (response.token !== undefined) {
                        localStorage.setItem('user', response.token)
                        localStorage.setItem('isUserLoggedIn', '1')
                    }
                }
            }
        }
    }

    async register() {
        const option = {
            method: "POST",
            body: this.prepareData(),
            headers: {
                'Accept': 'application/json, text/plain',
                'Content-Type': 'application/json;charset=UTF-8'
            }
        }
        const result = await fetch("http://127.0.0.1:8000/account/auth/", option)
        const response = await result.json()
        return response
    }

    prepareData = () => {
        const {account} = this.state
        const data = JSON.stringify({
            email: account.email,
            password: account.password
        })
        return data
    }
    validate = () => {
        const result = Joi.validate(this.state.account, this.schema, {abortEarly: false});
        if (!result.error) return null;
        const errors = {};
        for (let item of result.error.details)
            errors[item.path[0]] = item.message;
        const state = {...this.state}
        state["errors"] = errors
        this.setState(state)
    }

    render() {
        const {account} = this.state
        if (localStorage.getItem('isUserLoggedIn') === '1'){
            console.log('loged')
            // <Redirect to='/' />
        }
        return (
            <div className='card w-50 text-right mx-auto mt-3'>
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
                            <label htmlFor="re_password">تکرار کلمه عبور</label>
                            <input onChange={this.handleChange} value={account.re_password} type='password'
                                   className='form-control'
                                   id='re_password'/>
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

export default Register;