import React, {Component} from 'react';
import {Link, withRouter} from "react-router-dom"
import Product from "./Product";
import Breadcumb from "./Breadcumb";
import Subcategory from "./Subcategory";

class Category extends Component {
    constructor(props) {
        super(props);
        this.get_products = this.get_products.bind(this)
    }

    state = {
        children_category: [],
        parent_category: [],
        products: [],
        page: 1,
        per_page: 3,
        order_by: "created_time",
        total_products: 0,
        showing_products: [],
        number_of_pages: 1
    }

    async get_category() {
        const parents_raw = await fetch(`http://127.0.0.1:8000/category/${this.props.match.params.id}/all_parents/?self`)
        const parents = await parents_raw.json()
        const state_parent = []
        for (let parent of parents) {
            state_parent.push(parent)
        }
        const children_raw = await fetch(`http://127.0.0.1:8000/category/${this.props.match.params.id}/children/`)
        const children = await children_raw.json()
        const children_state = []
        for (let child of children) {
            children_state.push(child)
        }

        this.setState({
            parent_category: state_parent,
            children_category: children_state
        })

    }

    async get_products() {
        const url = `http://127.0.0.1:8000/product/find/?category=${this.props.match.params.id}&sortby=-${this.state.order_by}&recursive=true`
        const products_raw = await fetch(url)
        const products = await products_raw.json()
        const state_product = []
        for (let product of products) {
            state_product.push(product)
        }
        this.setState({products: state_product})
        this.setState({total_products: state_product.length})
        if(state_product.length>0){
            this.setState({number_of_pages: Math.ceil(state_product.length / this.state.per_page)})
            this.generateProductsToShow()
        }else{
            this.setState({showing_products:[]})
        }


    }

    generateProductsToShow = () => {
        var products = []
        for (let i = this.state.page * this.state.per_page - this.state.per_page; i < this.state.page * this.state.per_page; i++) {
            if (i<this.state.total_products){
                products.push(this.state.products[i])
            }

        }
        this.setState({showing_products: products})
    }

    componentDidMount() {
        this.get_category()
        this.get_products()
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (prevProps.match.params.id !== this.props.match.params.id) {
            this.get_category()
            this.get_products()
        } else {
            if (prevState.page !== this.state.page || prevState.per_page !== this.state.per_page) {
                this.get_products()
            }
        }
    }

    generateClassFirstItem = () => {
        if (this.state.page === 1) {
            return "page-item disabled"
        } else {
            return "page-item"
        }
    }
    generateClassLastItem = () => {
        if (this.state.page === this.state.number_of_pages) {
            return "page-item disabled"
        } else {
            return "page-item"
        }
    }
    getItemClasses = (page) => {
        if (page === this.state.page) {
            return "page-item active"
        } else {
        }
        return "page-item"
    }
    setPage = (page) => {
        if (page === "next") {
            if(this.state.page < this.state.number_of_pages){
                this.setPage(this.state.page+1)
            }
        } else if (page === "prev") {
            if(this.state.page !== 1){
                this.setPage(this.state.page-1)
            }
        } else {
            this.setState({page: page})
        }

    }
    generatePagination = () => {
        if (this.state.page === 1) {
            if (this.state.number_of_pages === 1) {
                var pages = [1]
            } else if (this.state.number_of_pages === 2) {
                var pages = [1, 2]
            } else if (this.state.number_of_pages === 3) {
                var pages = [1, 2, 3]
            }
        } else if (this.state.page === 2) {
            if (this.state.number_of_pages === 2) {
                var pages = [1, 2]
            } else {
                var pages = [1, 2, 3]
            }
        } else {
            if (this.state.number_of_pages >= this.state.page + 1) {
                var pages = [this.state.page - 1, this.state.page, this.state.page + 1]
            } else {
                var pages = [this.state.page - 1, this.state.page]
            }

        }
        return (
            <nav aria-label="...">
                <ul className="pagination rtl">

                    <li className={this.generateClassFirstItem()}>
                        <a  onClick={() => this.setPage("prev")} className="page-link"  tabIndex="-1">قبلی</a>
                    </li>
                    {pages.map((page, index) => {
                        return <li key={index} className={this.getItemClasses(page)}>
                            <a onClick={() => this.setPage(page)} className="page-link">{page}</a>
                        </li>
                    })}

                    <li className={this.generateClassLastItem()}>
                        <a onClick={() => this.setPage("next")} className="page-link"  tabIndex="-1">بعدی</a>
                    </li>
                </ul>
            </nav>
        )
    }

    render() {
        // this.call_server()
        return (
            <>
                <div className='not-rtl'>
                    <Breadcumb parents={this.state.parent_category}/>
                </div>
                {/* eslint-disable-next-line array-callback-return */}
                <div className='row'>
                    <div className='col-12 col-md-3 '>
                        <Subcategory subcategories={this.state.children_category}/>
                    </div>
                    <div className='col-md-9'>
                        <div className='row'>
                            {this.state.showing_products.map((product, index) => {
                                return (
                                    <>
                                        <Product key={index} name={product.name}
                                                 image={`http://127.0.0.1:8000${product.image}`}
                                                 price={product.price}
                                                 product_id={product.id}
                                                 quantity={product.quantity}/>
                                    </>
                                )
                            })}
                        </div>
                    </div>
                </div>
                <div className='row'>
                    {this.generatePagination()}
                </div>
            </>
        );
    }
}

export default withRouter(Category);