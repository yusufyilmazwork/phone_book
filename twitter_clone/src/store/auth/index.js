import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    currentAccount: {
       id: 1,
       username: "asdffda",
       fullName: "full+full",
        avatar: "https://images.pexels.com/photos/771742/pexels-photo-771742.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
    },
    accounts: [
        {
            id: 1,
            username: "asdffda",
            fullName: "full+full",
             avatar: "https://images.pexels.com/photos/771742/pexels-photo-771742.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
         },
        {
            id: 2,
            username: "fffffda",
            fullName: "fulll+full",
             avatar: "https://images.pexels.com/photos/771742/pexels-photo-771742.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
         },
    ]
}

const auth = createSlice({
    name : "auth",
    initialState,
    reducers: {
        _addAccount: (state, action) => {
            state.accounts.push(action.payload)
        },
        _removeAccount: (state, action) => {
            state.accounts = state.accounts.filter(account => account.id !== action.payload)
            if(state.currentAccount && action.payload === state.currentAccount.id){
                this._setCurrentAccount(false)
            }
        },
        _setCurrentAccount: (state, action) => {
            state.currentAccount = action.payload
        }
    }
})

export const {_addAccount, _setCurrentAccount, _removeAccount} = auth.actions
export default auth.reducer