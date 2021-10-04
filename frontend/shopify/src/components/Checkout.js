import React, {Component} from 'react';
import Operator from "./Operator";
import {Link, withRouter, Redirect} from "react-router-dom";
import User from "./User";

class Checkout extends Component {
    state = {
        discount: "",
        discountValidation: "",
        discountPercent: 0,
        option: "",
        option_type: "",
        option_price: "",
        address_to_send: "",
        address_to_invoice: "",
        delivery: "",
        delivery_price: ""

    }

    changeDelivery = (delivery) => {
        this.setState({delivery: delivery['id'], delivery_price: delivery['price']})
    }
    changeAddressToSend = (address) => {
        this.setState({address_to_send: address})
    }
    changeAddressToInvoice = (address) => {
        this.setState({address_to_invoice: address})
    }
    changeOption = (option) => {
        this.setState({option: option['id'], option_type: option['type'], option_price: option['price']})
    }

    totalPrice = () => {
        if (this.props.orders) {
            var price = 0
            for (let order of this.props.orders) {
                console.log(order)
                price = price + order.price * order.quantity
            }
            return price
        }
    }
    totalPriceWithDiscount = () => {
        const totalPrice = this.totalPrice()
        const withDiscount = totalPrice * (100 - this.state.discountPercent) / 100
        return withDiscount
    }

    finalPrice = () => {
        window.basic = 0
        if (this.state.discountValidation) {
            window.basic = this.totalPriceWithDiscount()
        } else {
            window.basic = this.totalPrice()
        }
        if (this.state.option_type == 0) {

            window.option_price = window.basic * (1 + Number(this.state.option_price) / 100)
        } else {
            window.option_price = window.basic + Number(this.state.option_price)
        }
        return parseInt((window.option_price + Number(this.state.delivery_price)))
    }
    generateAllTable = () => {
        return (
            <tr>
                <td>جمع کل کالا:</td>
                <td>{this.totalPrice()}</td>
                <td></td>
                <td></td>
                <td></td>
            </tr>
        )
    }
    generateDiscountTable = () => {
        return (
            <tr>
                <td>تخفیف:</td>
                <td>{parseInt(this.totalPrice() * this.state.discountPercent / 100)}</td>
                <td></td>
                <td></td>
                <td></td>
            </tr>
        )
    }
    generateDeliveryTable = () => {
        return (
            <tr>
                <td>هزینه ارسال:</td>
                <td>{this.state.delivery_price}</td>
                <td></td>
                <td></td>
                <td></td>
            </tr>
        )
    }
    generateOptionTable = () => {
        window.basic = 0
        if (this.state.discountValidation) {
            window.basic = this.totalPriceWithDiscount()
        } else {
            window.basic = this.totalPrice()
        }
        if (this.state.option_type == 0) {

            window.option_price = window.basic * Number(this.state.option_price) / 100
        } else {
            window.option_price = Number(this.state.option_price)
        }

        return (
            <tr>
                <td>هزینه خدمات:</td>
                <td>{parseInt(window.option_price)}</td>
                <td></td>
                <td></td>
                <td></td>
            </tr>
        )
    }
    generateList = () => {
        return (


            <table className="table">
                <thead>
                <tr>

                    <th scope="col">نام محصول</th>
                    <th scope="col">تعداد</th>
                    <th scope="col">قیمت واحد</th>
                    <th scope="col">قیمت کل</th>
                    <th scope="col"/>
                </tr>
                </thead>
                <tbody>
                {this.props.orders && this.props.orders.map((order, index) => {
                    return (
                        <tr key={index}>
                            <td>{order.name}</td>
                            <td>{order.quantity}</td>
                            <td>{order.price}</td>
                            <td>{order.price * order.quantity}</td>
                            <td><Operator id={index} orders={this.props.orders} updateOrder={this.props.updateOrder}/>
                            </td>

                            {/*<li key={index} className="list-group-item">{order.name} {order.quantity}<Operator/></li>*/}
                        </tr>
                    )
                })}
                {this.generateAllTable()}
                {this.state.discountValidation && this.generateDiscountTable()}
                {this.generateDeliveryTable()}
                {this.generateOptionTable()}
                <tr>
                    <td>مبلغ قابل پرداخت:</td>
                    <td>{this.finalPrice()}</td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>

                </tbody>
            </table>

        )
    }
    handleChange = ({currentTarget: input}) => {
        this.setState({discount: input.value})
    }
    checkDiscount = () => {
        const option = {
            method: "GET",
            headers: {
                'Accept': 'application/json, text/plain',
                'Content-Type': 'application/json;charset=UTF-8',
                'Authorization': `token ${this.props.user ? this.props.user : localStorage.getItem('user')}`
            }
        }
        console.log(option)
        const url = `http://127.0.0.1:8000/card/card/discount_validation/?code=${this.state.discount}`
        fetch(url, option).then(response => response.json()).then(data => this.handleValidation(data))
    }
    handleValidation = (data) => {
        if (data.status) {
            this.setState({discountValidation: data.status, discountPercent: data.percent})
            let card = localStorage.getItem('card')
            card = JSON.parse(card)
            card['discount'] = this.state.discount
            localStorage.setItem('card', JSON.stringify(card))

        } else {
            this.setState({discountValidation: false})
        }
    }

    generateCheckout = () => {
        return (
            <>
                <label htmlFor='discount'>کد تخفیف</label>
                <input type="text" id='discount' name="discount" value={this.state.discount}
                       onChange={this.handleChange}/>
                <button className='btn btn-primary' onClick={this.checkDiscount}>ثبت</button>
                {console.log(this.state.discountValidation)}
                {this.state.discountValidation && <h1>yes</h1>}
                {!this.state.discountValidation && <h1>No</h1>}
                {this.generateUser()}
            </>

        )
    }


    generateLog = () => {
        this.props.redirectTo('/checkout')
        return (
            <>
                <Link to='/login'> ورود </Link>
                <Link to="/register"> ثبت نام </Link>
            </>
        )
    }


    generateUser = () => {
        return <User delivery={this.changeDelivery}
                     option={this.changeOption}
                     send={this.changeAddressToSend}
                     invoice={this.changeAddressToInvoice}
                     user={this.props.user}/>

    }
    information = () => {
        if (this.props.loggedIn) {

            return this.generateCheckout()

        } else {
            return this.generateLog()
        }
    }
    addCard = () => {
        const data = {
            discount: this.reformatDiscount(),
            additional_option: this.state.option,
            delivery: this.state.delivery,
            address_to_send_good: this.state.address_to_send,
            address_to_send_invoice: this.state.address_to_invoice,
            receive_time: "2021-11-18 13:24:46",
            orders: this.reformatOrders(),
            payment_info: 1
        }
        const option = {
            method: "POST",
            body: JSON.stringify(data),
            headers: {
                'Accept': 'application/json, text/plain',
                'Content-Type': 'application/json;charset=UTF-8',
                'Authorization': `token ${this.props.user ? this.props.user : localStorage.getItem('user')}`
            }
        }
        const url = 'http://127.0.0.1:8000/card/card/'
        fetch(url, option).then(response => response.json()).then(data => this.cardAdded(data))
    }
    reformatDiscount = () => {
        if (this.state.discountValidation === true) {
            return this.state.discount
        } else {
            return false
        }
    }
    reformatOrders = () => {
        var final_order_list = []
        for (let order of this.props.orders) {
            if (order.option) {
                final_order_list.push({product: order.product, quantity: order.quantity, option: order.option})
            } else {
                final_order_list.push({product: order.product, quantity: order.quantity})
            }
        }
        return final_order_list
    }
    cardAdded = (data) => {
        if (data.orders) {
            localStorage.removeItem('card')
            this.props.updateOrder([])
        }
    }


    render() {
        return (
            <div>
                {this.generateList()}
                {this.information()}
                {this.props.orders.length > 0 && this.props.loggedIn &&
                <button onClick={this.addCard} className='btn btn-primary'>پرداخت</button>}
                {/*{this.props.loggedIn && this.generateCheckout() || this.generateLog()}*/}


            </div>
        );
    }

    async componentDidMount() {
        let card = localStorage.getItem('card')
        card = JSON.parse(card)
        if (card && card['discount']) {
            await this.setState({discount: card['discount']})
            this.checkDiscount()
        }
    }

}

export default withRouter(Checkout);