import React, {Component} from 'react';
import './Register.css';
import Joi from 'joi-browser'
import {Redirect} from "react-router-dom";


class Register extends Component {
    constructor(props) {

        super(props);
        this.handleSubmit = this.handleSubmit.bind(this)
        this.register = this.register.bind(this)

    }

    state = {
        account: {
            email: "",
            password: "",
            re_password: ""
        },
        errors: {},
        redirect: false,
        is_admin: false,
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
                        const state = {...this.state}
                        state['redirect'] = true
                        this.props.handleStatus(true)
                        if(this.state.is_admin === true){
                            localStorage.setItem('user_permission','store_admin')
                            this.props.set_user_permission('store_admin')
                        }else {
                            localStorage.setItem('user_permission','customer')
                            this.props.set_user_permission('customer')
                        }

                        this.setState(state)
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
        return await result.json()
    }

    prepareData = () => {
        const {account} = this.state
        return JSON.stringify({
            email: account.email,
            password: account.password,
            user_type : this.state.is_admin ? 2 : 0
        })
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

    redirectToHome = () => {
        return <Redirect to={`/${this.props.redirectTo}`}/>
    }

    handleClick = () => {
        this.setState({is_admin: !this.state.is_admin})
    }


    render() {
        const {account} = this.state
        if (localStorage.getItem('isUserLoggedIn') === "1") {
            const state = {...this.state}
            state['redirect'] = true
            this.setState(state)
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
                            <label htmlFor="re_password">تکرار کلمه عبور</label>
                            <input onChange={this.handleChange} value={account.re_password} type='password'
                                   className='form-control'
                                   id='re_password'/>
                            <label htmlFor="admin">به عنوان فروشنده</label>
                            <input defaultChecked={this.state.is_admin} onClick={this.handleClick} type="checkbox"
                                   name='admin' id='admin'/>

                        </div>
                        <button type="submit" className="btn btn-primary">Submit</button>
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