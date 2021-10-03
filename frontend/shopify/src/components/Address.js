import React, {Component} from 'react';

class Address extends Component {
    state = {
        address: "",
        postal_code: ""
    }
    addNewAddressOption = (data) => {
        if (data.address) {
            this.props.refresh()
            this.setState({address: "", postal_code: ""})
        }
    }
    handleAddAddress = () => {
        const url = "http://127.0.0.1:8000/account/address/"
        const data = {
            address: this.state.address,
            postal_code: this.state.postal_code
        }
        console.log(data)
        const option = {
            method: "POST",
            body: JSON.stringify(data),
            headers: {
                'Accept': 'application/json, text/plain',
                'Content-Type': 'application/json;charset=UTF-8',
                'Authorization': `token ${this.props.user ? this.props.user : localStorage.getItem('user')}`
            }
        }


        if (this.state.address !== "" && this.state.postal_code !== "") {
            fetch(url, option).then(response => response.json()).then(data => this.addNewAddressOption(data))
        }
    }

    handleInputAddress = ({currentTarget: input}) => {
        this.setState({address: input.value})
    }
    handleInputPostal = ({currentTarget: input}) => {
        this.setState({postal_code: input.value})
    }

    handleInvoiceAddressChange = (e) => {
        this.props.invoice(e.target.value)
    }
    handleSendAddressChange = (e) => {
        this.props.send(e.target.value)
    }

    generateAddress = () => {
        return (
            <>
                <label htmlFor="send_good">آدرس ارسال محصول</label>
                <select onClick={this.handleInvoiceAddressChange} name="send_good" id='send_good'>
                    {this.props.address.length > 0 && this.props.address.map((address, index) => {
                        return <option key={index} name={address.id} value={address.id}>{address.address}</option>
                    })}
                </select>
                <label htmlFor="send_invoice">آدرس ارسال فاکتور</label>
                <select onClick={this.handleSendAddressChange} name="send_invoice" id='send_good'>
                    {this.props.address.length > 0 && this.props.address.map((address, index) => {
                        return <option key={index} name={address.id} value={address.id}>{address.address}</option>
                    })}
                </select>

                <label htmlFor="add_new_address">آدرس</label>
                <input onChange={this.handleInputAddress} name='add_new_address' id='add_new_address'
                       value={this.state.address}/>
                <label htmlFor="add_new_postal">کد پستی</label>
                <input onChange={this.handleInputPostal} type='number' name='add_new_postal' id='add_new_postal'
                       value={this.state.postal_code}/>
                <button onClick={this.handleAddAddress} className='btn btn-primary'>افزودن آدرس جدید</button>
            </>
        )
    }

    render() {
        return (
            <div>
                {this.generateAddress()}
            </div>
        );
    }
}

export default Address;